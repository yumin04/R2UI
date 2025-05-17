from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color
from kivy.clock import Clock
from kivy.graphics import Color, Line
from kivy.uix.floatlayout import FloatLayout


class ToggleView(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.toggle_options = ["Light: ON", "Movement: LOCKED"]
        self.build_back_button()
        self.build_UI_for_toggle()
        self.index_lower_bound = -1
        self.index_upper_bound = len(self.toggle_options)

    def build_UI_for_toggle(self):
        self.fixed_area = GridLayout(
            size_hint=(0.45, 0.75),
            cols=2,
            rows=1,
            spacing=10,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.left_toggle = Button(
            text=self.toggle_options[0],
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.75, "center_y": 0.9},
            font_size=20,
            color=(0, 0, 0, 1),
            background_normal="",
            background_color=(1, 1, 1, 1),
        )
        self.right_toggle = Button(
            text=self.toggle_options[1],
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.75, "center_y": 0.9},
            font_size=20,
            color=(0, 0, 0, 1),
            background_normal="",
            background_color=(1, 1, 1, 1),
        )

        self.fixed_area.add_widget(self.left_toggle)
        self.fixed_area.add_widget(self.right_toggle)
        self.add_widget(self.fixed_area)
        self.cover_cell(0)

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

    def spinner_click(self, index):
        if index == -1:
            return "back"
        if index == 0:
            current = self.left_toggle.text
            self.left_toggle.text = (
                "Light: OFF" if current == "Light: ON" else "Light: ON"
            )
        elif index == 1:
            current = self.right_toggle.text
            self.right_toggle.text = (
                "Movement: UNLOCKED"
                if current == "Movement: LOCKED"
                else "Movement: LOCKED"
            )
        return "button"

    def cover_cell(self, index):
        self._remove_border_from_button(self.left_toggle)
        self._remove_border_from_button(self.right_toggle)

        if index == -1:
            self.select_back_button()
            return

        self.unselect_back_button()

        def draw_border(_dt):
            if index == 0:
                target = self.left_toggle
            else:
                target = self.right_toggle
            with target.canvas.after:
                Color(1, 0, 0, 1)
                Line(
                    rectangle=(target.x, target.y, target.width, target.height),
                    width=2,
                )

        Clock.schedule_once(draw_border, 0)

    def _remove_border_from_button(self, button):
        canvas = button.canvas.after
        to_remove = []
        for instr in canvas.children:
            if isinstance(instr, Line) or isinstance(instr, Color):
                to_remove.append(instr)
            if len(to_remove) >= 2:
                break
        for instr in to_remove:
            canvas.remove(instr)

    def select_back_button(self):
        self.back_button.background_normal = "assets/BackButtonSelected.png"
        self.back_button.background_down = "assets/BackButtonSelected.png"

    def unselect_back_button(self):
        self.back_button.background_normal = "assets/BackButton.png"
        self.back_button.background_down = "assets/BackButton.png"

    def make_selection_transparent(self):
        self.left_toggle.background_color = (1, 1, 1, 0)
        self.right_toggle.background_color = (1, 1, 1, 0)

    def make_selection_untransparent(self):
        self.left_toggle.background_color = (1, 1, 1, 1)
        self.right_toggle.background_color = (1, 1, 1, 1)
