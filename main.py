from kivy.config import Config

Config.set("graphics", "width", "800")
Config.set("graphics", "height", "480")
# Config.set("graphics", "borderless", "1")
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.metrics import dp
import serial
from kivy.core.audio import SoundLoader
from functools import partial
from kivy.graphics import PushMatrix, PopMatrix, Scale


class HighlightedImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 0, 0.3)  # 노란색 배경, 30% 투명도
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


try:
    ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
except Exception as e:
    ser = None
    print(f"[WARNING] Serial not connected: {e}")


Builder.load_file("main.kv")


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.global_index = 0
        self.HP_index = 0
        self.emotions = [
            ("Scared", "Scared.png", (0.16, 0.84)),
            ("Neutral", "Neutral.png", (0.5, 0.84)),
            ("Confused", "Confused.png", (0.84, 0.84)),
            ("Sad", "Sad.png", (0.16, 0.5)),
            ("Happy", "Happy.png", (0.5, 0.5)),
            ("Angry", "Angry.png", (0.84, 0.5)),
            ("Nervous", "Nervous.png", (0.16, 0.16)),
            ("Curious", "Curious.png", (0.5, 0.16)),
            ("Proud", "Proud.png", (0.84, 0.16)),
        ]

    # build general ui

    def build_fixed_grid(self):
        self.ids.fixed_area.clear_widgets()
        for label, img, position in self.emotions:
            btn = Button(
                background_normal=f"assets/R2Emotion/{img}",
                background_down=f"assets/R2Emotion/{img}",
                size_hint=(0.33, 0.33),
                on_press=lambda instance, val=label: self.send_emotion_signal(val),
            )
            self.ids.fixed_area.add_widget(btn)
        self.cover_cell(self.global_index)

    def build_panther_left_and_right(self):
        scale = 2
        y_pos = 0.23
        panther_left = Image(
            source="assets/PantherSingleLeft.png",
            size_hint=(scale, scale),
            pos_hint={"center_x": 0.5, "center_y": y_pos},
        )
        panther_right = Image(
            source="assets/PantherSingleRight.png",
            size_hint=(scale, scale),
            pos_hint={"center_x": 0.5, "center_y": y_pos},
        )
        self.ids.panther_left.add_widget(panther_left)
        self.ids.panther_right.add_widget(panther_right)

    def cover_cell(self, index):
        x = self.emotions[index][2][0]
        y = self.emotions[index][2][1]
        paw_x = x - 0.145
        paw_y = y - 0.1
        cover = self.ids.button_cover
        cover.pos_hint = {"center_x": x, "center_y": y}
        cover.background_normal = (
            f"assets/R2EmotionSelected/{self.emotions[index][0]}Selected.png"
        )
        cover.background_down = (
            f"assets/R2EmotionSelected/{self.emotions[index][0]}Selected.png"
        )
        paw = self.ids.button_cover_paw
        paw.pos_hint = {"center_x": paw_x, "center_y": paw_y}

    def build_top_ui(self):
        # 첫 번째 버튼 - Wifi
        wifi_button = Button(
            background_normal="assets/Wifi.png",
            background_down="assets/Wifi.png",
            size_hint=(None, None),
            size=(40, 40),
        )
        self.ids.top_ui_buttons.add_widget(wifi_button)

        # 두 번째 버튼 - Signal
        signal_button = Button(
            background_normal="assets/Signal.png",
            background_down="assets/Signal.png",
            size_hint=(None, None),
            size=(40, 40),
        )
        self.ids.top_ui_buttons.add_widget(signal_button)

        # 세 번째 버튼 - R2
        r2_button = Button(
            background_normal="assets/R2.png",
            background_down="assets/R2.png",
            size_hint=(None, None),
            size=(40, 40),
        )
        self.ids.top_ui_buttons.add_widget(r2_button)

    # delete when no memory
    def add_panther_buttons(self):
        left_button = Button(
            text="<",
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_normal="",
            background_color=(0.6, 0.6, 0.6, 0.8),
            on_press=lambda instance: self.spinner_left(),
        )
        self.ids.panther_left.add_widget(left_button)

        right_button = Button(
            text=">",
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_normal="",
            background_color=(0.6, 0.6, 0.6, 0.8),
            on_press=lambda instance: self.spinner_right(),
        )
        self.ids.panther_right.add_widget(right_button)

    # input logic
    def spinner_right(self):
        if self.global_index < len(self.emotions) - 1:
            self.global_index += 1
            self.cover_cell(self.global_index)

    def spinner_left(self):
        if self.global_index > 0:
            self.global_index -= 1
            self.cover_cell(self.global_index)

    def spinner_click(self):
        emotion_name, _ = self.emotions[self.global_index]
        self.send_emotion_signal(emotion_name)

    def HP_joystick_click(self):
        if self.HP_index == 0:
            self.HP_index = 1
            self.send_HP_change_signal()
            print("joystick clicked")
        else:
            self.HP_index = 0
            self.send_HP_change_signal()
            print("joystick clicked")

    def send_HP_change_signal(self):
        self.ids.what_HP.text = f"Current HP: {self.HP_index}"

    def send_emotion_signal(self, emotion_name, *args):
        print(f"[SOUND] Playing emotion: {emotion_name}")
        sound = SoundLoader.load(f"sounds/{emotion_name.lower()}.mp3")
        if sound:
            sound.play()
        else:
            print(f"[ERROR] Sound not found: {emotion_name}")

    # connection UI logic
    def connected_wifi(self):
        self.ids.wifi_button.source = "assets/Wifi.png"

    def disconnected_wifi(self):
        self.ids.wifi_button.source = "assets/NoWifi.png"

    def connected_R2(self):
        self.ids.r2_button.source = "assets/R2.png"

    def disconnected_R2(self):
        self.ids.r2_button.source = "assets/NoR2.png"


class R2UIApp(App):
    def build(self):
        screen = MainScreen()
        screen.build_fixed_grid()
        screen.build_panther_left_and_right()

        # UI logic are these functions, if any of the things are connected/disconnected
        # we can use these 4 functions to change the images
        # TODO: delete
        screen.connected_R2()
        screen.connected_wifi()
        screen.disconnected_R2()
        screen.disconnected_wifi()

        # If this is deleted, then left and right button deletes
        # so delete this when putting into screen
        # TODO: delete
        screen.add_panther_buttons()
        return screen


if __name__ == "__main__":
    R2UIApp().run()
