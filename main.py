from kivy.config import Config

Config.set("graphics", "width", "800")
Config.set("graphics", "height", "480")
# Config.set("graphics", "borderless", "1")
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
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


# class HighlightedImage(Image):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         with self.canvas.before:
#             Color(1, 1, 0, 0.3)  # 노란색 배경, 30% 투명도
#             self.bg_rect = Rectangle(pos=self.pos, size=self.size)
#         self.bind(pos=self.update_bg, size=self.update_bg)

#     def update_bg(self, *args):
#         self.bg_rect.pos = self.pos
#         self.bg_rect.size = self.size


try:
    ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
except Exception as e:
    ser = None
    print(f"[WARNING] Serial not connected: {e}")

from kivy.uix.screenmanager import ScreenManager, Screen


class GeneralUI(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background()
        self.initialize_top_ui()
        self.left_and_right_panther_layout()
        self.build_panther_left_and_right()
        self.build_back_button()

    def background(self):
        # 배경 이미지
        with self.canvas.before:
            self.bg_rect = Rectangle(
                source="assets/Background.png",
                pos=self.pos,
                size=self.size,
            )
            self.bind(pos=self.update_rect, size=self.update_rect)

    def initialize_top_ui(self):
        # top_ui 전체 floatlayout
        self.top_ui = FloatLayout(
            size_hint=(None, 0.1),
            size=(700, 46),
            pos_hint={"center_x": 0.5, "center_y": 0.9375},
        )

        with self.top_ui.canvas.before:
            Color(1, 1, 1, 1)
            self.top_ui.bg_rect = Rectangle(
                source="assets/TopUI.png",
                pos=self.top_ui.pos,
                size=self.top_ui.size,
            )
            self.top_ui.bind(pos=self.update_top_ui, size=self.update_top_ui)

        # 버튼 4개 있는 그리드
        self.top_ui_buttons = GridLayout(
            cols=4,
            spacing=6,
            size_hint=(None, None),
            size=(144, 32),  # 32*4 + 6*3
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.top_wifi = Image(
            source="assets/Wifi.png",
            size_hint=(None, None),
            size=(32, 32),
        )
        self.top_signal = Image(
            source="assets/Signal.png",
            size_hint=(None, None),
            size=(32, 32),
        )

        self.top_R2 = Image(
            source="assets/R2.png",
            size_hint=(None, None),
            size=(32, 32),
        )
        self.top_ui_buttons.add_widget(self.top_wifi)
        self.top_ui_buttons.add_widget(self.top_signal)
        self.top_ui_buttons.add_widget(self.top_R2)

        self.top_ui.add_widget(self.top_ui_buttons)
        self.add_widget(self.top_ui)

    def left_and_right_panther_layout(self):
        # panther_left
        self.panther_left = FloatLayout(
            size_hint=(0.275, 1),
            pos_hint={"center_x": 0.1375, "center_y": 0.5},
        )
        self.add_widget(self.panther_left)

        # panther_right
        self.panther_right = FloatLayout(
            size_hint=(0.275, 1),
            pos_hint={"center_x": 0.8625, "center_y": 0.5},
        )
        self.add_widget(self.panther_right)

    def build_back_button(self):
        self.back_button = Button(
            background_normal="assets/BackButton.png",
            background_down="assets/BackButton.png",
            pos_hint={"center_x": 0.5, "center_y": 0.75},
            size_hint=(0.35, 0.165),
        )
        self.panther_left.add_widget(self.back_button)

    def cover_back_button(self):
        self.back_button.background_normal = "assets/BackButtonSelected.png"
        self.back_button.background_down = "assets/BackButtonSelected.png"

    def uncover_back_button(self):
        self.back_button.background_normal = "assets/BackButton.png"
        self.back_button.background_down = "assets/BackButton.png"

    def build_panther_left_and_right(self):
        scale = 2
        y_pos = 0.23
        left_panther = Image(
            source="assets/PantherSingleLeft.png",
            size_hint=(scale, scale),
            pos_hint={"center_x": 0.5, "center_y": y_pos},
        )
        right_panther = Image(
            source="assets/PantherSingleRight.png",
            size_hint=(scale, scale),
            pos_hint={"center_x": 0.5, "center_y": y_pos},
        )
        self.panther_left.add_widget(left_panther)
        self.panther_right.add_widget(right_panther)

    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def update_top_ui(self, instance, *args):
        instance.bg_rect.pos = instance.pos
        instance.bg_rect.size = instance.size

    # connection UI logic
    def connected_wifi(self):
        self.top_wifi.source = "assets/Wifi.png"

    def disconnected_wifi(self):
        self.top_wifi.source = "assets/NoWifi.png"

    def connected_R2(self):
        self.top_R2.source = "assets/R2.png"

    def disconnected_R2(self):
        self.top_R2.source = "assets/NoR2.png"

    def HP_joystick_click(self):
        if self.HP_index == 0:
            self.HP_index = 1
            self.send_HP_change_signal()
            print("joystick clicked")
        else:
            self.HP_index = 0
            self.send_HP_change_signal()
            print("joystick clicked")


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ui = GeneralUI()
        self.add_widget(self.ui)
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

    # build UI for Audio
    def build_UI_for_audio(self):
        self.build_fixed_grid()
        self.create_cover()

    def build_fixed_grid(self):
        self.fixed_area = GridLayout(
            size_hint=(0.45, 0.75),
            cols=3,
            rows=3,
            spacing=10,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        for label, img, position in self.emotions:
            btn = Button(
                background_normal=f"assets/R2Emotion/{img}",
                background_down=f"assets/R2Emotion/{img}",
                size_hint=(0.33, 0.33),
                on_press=lambda instance, val=label: self.send_emotion_signal(val),
            )
            self.fixed_area.add_widget(btn)
        self.add_widget(self.fixed_area)

    def create_cover(self):
        self.build_dynamic_area()
        self.create_selected_image_with_paw()

    def build_dynamic_area(self):
        self.dynamic_area = FloatLayout(
            size_hint=(0.45, 0.75), pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.add_widget(self.dynamic_area)

    def get_selected_index(self, index):
        x = self.emotions[index][2][0]
        y = self.emotions[index][2][1]
        paw_x = x - 0.145
        paw_y = y - 0.1
        background_normal = (
            f"assets/R2EmotionSelected/{self.emotions[index][0]}Selected.png"
        )
        background_down = (
            f"assets/R2EmotionSelected/{self.emotions[index][0]}Selected.png"
        )
        return x, y, paw_x, paw_y, background_normal, background_down

    def create_selected_image_with_paw(self):
        x, y, paw_x, paw_y, this_background_normal, this_background_down = (
            self.get_selected_index(0)
        )
        self.button_cover = Button(
            size_hint=(0.33, 0.33),
            background_normal=this_background_normal,
            background_down=this_background_down,
            pos_hint={"center_x": x, "center_y": y},
        )
        self.button_cover_paw = Button(
            size_hint=(0.2, 0.22),
            background_normal="assets/R2EmotionSelected/Paw.png",
            background_down="assets/R2EmotionSelected/Paw.png",
            pos_hint={"center_x": paw_x, "center_y": paw_y},
        )
        self.dynamic_area.add_widget(self.button_cover)
        self.dynamic_area.add_widget(self.button_cover_paw)

    def cover_cell(self, index):
        if index == -1:
            self.select_back_button()
            return
        self.unselect_back_button()
        x, y, paw_x, paw_y, this_background_normal, this_background_down = (
            self.get_selected_index(index)
        )
        self.button_cover.background_normal = this_background_normal
        self.button_cover.background_down = this_background_down
        self.button_cover.pos_hint = {"center_x": x, "center_y": y}
        self.button_cover_paw.pos_hint = {"center_x": paw_x, "center_y": paw_y}

    def select_back_button(self):
        self.ui.cover_back_button()
        self.make_selection_transparent()

    def unselect_back_button(self):
        self.ui.uncover_back_button()
        self.make_selection_untransparent()

    def make_selection_transparent(self):
        self.button_cover.background_color = (1, 1, 1, 0)

    def make_selection_untransparent(self):
        self.button_cover.background_color = (1, 1, 1, 1)

    def send_HP_change_signal(self):
        self.ids.what_HP.text = f"Current HP: {self.HP_index}"

    def send_emotion_signal(self, emotion_name, *args):
        print(f"[SOUND] Playing emotion: {emotion_name}")
        sound = SoundLoader.load(f"sounds/{emotion_name.lower()}.mp3")
        if sound:
            sound.play()
        else:
            print(f"[ERROR] Sound not found: {emotion_name}")

        # input logic

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
        self.ui.panther_left.add_widget(left_button)

        right_button = Button(
            text=">",
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_normal="",
            background_color=(0.6, 0.6, 0.6, 0.8),
            on_press=lambda instance: self.spinner_right(),
        )
        self.ui.panther_right.add_widget(right_button)

    def spinner_right(self):
        if self.global_index < len(self.emotions) - 1:
            self.global_index += 1
            self.cover_cell(self.global_index)

    def spinner_left(self):
        if self.global_index > -1:
            self.global_index -= 1
            self.cover_cell(self.global_index)

    def spinner_click(self):
        emotion_name, _ = self.emotions[self.global_index]
        self.send_emotion_signal(emotion_name)


class AudioScreen(Screen): ...


class HPScreen(Screen): ...


class R2UIApp(App):
    def build(self):
        screen = MainScreen()
        screen.build_UI_for_audio()
        screen.add_panther_buttons()
        # UI logic are these functions, if any of the things are connected/disconnected
        # we can use these 4 functions to change the images
        # # TODO: delete
        # screen.connected_R2()
        # screen.connected_wifi()
        # screen.disconnected_R2()
        # screen.disconnected_wifi()

        # If this is deleted, then left and right button deletes
        # so delete this when putting into screen
        # TODO: delete
        # screen.add_panther_buttons()
        return screen


if __name__ == "__main__":
    R2UIApp().run()
