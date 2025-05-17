from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle


class GeneralUI(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background()
        self.initialize_top_ui()
        self.left_and_right_panther_layout()
        self.build_panther_left_and_right()

    def background(self):
        with self.canvas.before:
            self.bg_rect = Rectangle(
                source="assets/Background.png",
                pos=self.pos,
                size=self.size,
            )
            self.bind(pos=self.update_rect, size=self.update_rect)

    def initialize_top_ui(self):
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

        self.top_ui_buttons = GridLayout(
            cols=4,
            spacing=6,
            size_hint=(None, None),
            size=(144, 32),
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
