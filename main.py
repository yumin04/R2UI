from kivy.config import Config

Config.set("graphics", "width", "800")
Config.set("graphics", "height", "480")

from kivy.app import App
from ui.screen_manager_ui import RootWidget


class R2UIApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    R2UIApp().run()
