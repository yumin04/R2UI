from kivy.uix.floatlayout import FloatLayout
from screens.main_view import MainView
from screens.audio_view import AudioView
from screens.toggle_view import ToggleView
from ui.general_ui import GeneralUI
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock


class RootWidget(Screen):  # 기존에는 FloatLayout이었음
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ui = GeneralUI()
        self.add_widget(self.ui)
        self.add_panther_buttons()

        self.content_area = FloatLayout(
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.add_widget(self.content_area)

        self.views = {
            "main": MainView(),
            "audio": AudioView(),
            "toggle": ToggleView(),
        }

        self.current_view = None
        self.global_index = 0
        self.screen_order = ["main", "audio", "toggle"]
        self.switch_view("main")  # default view

    def switch_view(self, name):
        self.global_index = 0
        if self.current_view:
            self.content_area.remove_widget(self.current_view)
        self.current_view = self.views[name]
        self.content_area.add_widget(self.current_view)

    def cover_cell(self):
        if self.current_view:
            self.current_view.cover_cell(self.global_index)

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
        click_button = Button(
            text="O",
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            background_normal="",
            background_color=(0.6, 0.6, 0.6, 0.8),
            on_press=lambda instance: self.spinner_click(),
        )
        self.ui.panther_left.add_widget(click_button)
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

    def spinner_click(self):
        if not self.current_view:
            return

        result = self.current_view.spinner_click(self.global_index)

        if result == "button":
            return
        elif result == "back":
            self.global_index = 0
            self.switch_view("main")
            Clock.schedule_once(lambda dt: self.cover_cell(), 0)
        elif result == "toggle":
            self.global_index = 1
            self.switch_view("toggle")
            Clock.schedule_once(lambda dt: self.cover_cell(), 0)
        elif result == "audio":
            self.global_index = 0
            self.switch_view("audio")
            Clock.schedule_once(lambda dt: self.cover_cell(), 0)

    def spinner_right(self):
        if (
            self.current_view
            and self.global_index < self.current_view.index_upper_bound
        ):
            self.global_index += 1
            self.cover_cell()

    def spinner_left(self):
        if (
            self.current_view
            and self.global_index > self.current_view.index_lower_bound
        ):
            self.global_index -= 1
            self.cover_cell()
