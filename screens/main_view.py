# screens/main_screen.py
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Line
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout


class MainView(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.index_lower_bound = 0
        self.index_upper_bound = 1
        self.build_UI_for_main()
        Clock.schedule_once(lambda dt: self.cover_cell(0), 1)

    def build_UI_for_main(self):
        self.build_fixed_grid()

    def build_fixed_grid(self):
        self.fixed_area = GridLayout(
            size_hint=(0.45, 0.75),
            cols=2,
            rows=1,
            spacing=10,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.to_toggle = Button(
            text="Toggle",
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.75, "center_y": 0.9},
            font_size=20,
            color=(0, 0, 0, 1),
            background_normal="",
            background_color=(1, 1, 1, 1),
        )
        self.to_audio = Button(
            text="Audio",
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.75, "center_y": 0.9},
            font_size=20,
            color=(0, 0, 0, 1),
            background_normal="",
            background_color=(1, 1, 1, 1),
        )
        self.fixed_area.add_widget(self.to_audio)
        self.fixed_area.add_widget(self.to_toggle)
        self.add_widget(self.fixed_area)

    def cover_cell(self, index):
        self._remove_border_from_button()

        if index == 0:
            target = self.to_audio
        else:
            target = self.to_toggle

        with target.canvas.after:
            self.border_color = Color(1, 0, 0, 1)
            self.border_line = Line(
                rectangle=(target.x, target.y, target.width, target.height),
                width=2,
            )

        self.border_canvas = target.canvas.after  # 보더가 올라간 canvas 저장

    def _remove_border_from_button(self):
        if hasattr(self, "border_line") and self.border_line and self.border_canvas:
            self.border_canvas.remove(self.border_line)
            self.border_line = None

        if hasattr(self, "border_color") and self.border_color and self.border_canvas:
            self.border_canvas.remove(self.border_color)
            self.border_color = None

    def spinner_click(self, index):
        if index == 0:
            return "audio"
        return "toggle"
