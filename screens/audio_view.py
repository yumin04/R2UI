from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen


class AudioView(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        self.index_lower_bound = -1
        self.index_upper_bound = len(self.emotions)
        self.build_UI_for_audio()
        self.build_back_button()

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

    def build_back_button(self):
        self.back_button_area = FloatLayout(
            size_hint=(None, None),
            size=(300, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.75},
        )

        self.back_button = Button(
            background_normal="assets/BackButton.png",
            background_down="assets/BackButton.png",
            size_hint=(0.35, 0.165),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.back_button_area.add_widget(self.back_button)
        self.add_widget(self.back_button_area)

    def cover_back_button(self):
        self.back_button.background_normal = "assets/BackButtonSelected.png"
        self.back_button.background_down = "assets/BackButtonSelected.png"

    def uncover_back_button(self):
        self.back_button.background_normal = "assets/BackButton.png"
        self.back_button.background_down = "assets/BackButton.png"

    def select_back_button(self):
        self.cover_back_button()
        self.make_selection_transparent()

    def unselect_back_button(self):
        self.uncover_back_button()
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

    def spinner_click(self):
        if self.global_index == -1:
            return "back"
        emotion_name, _, _ = self.emotions[self.global_index]
        self.send_emotion_signal(emotion_name)
        return "button"
