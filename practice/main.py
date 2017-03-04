from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

sm = ScreenManager()


class Main(Screen):
    def __init__(self):
        super(Main, self).__init__()


class Login(Screen):
    def __init__(self):
        super(Login, self).__init__()
        # Change login screen size in it's __init__
        update_window_size(250, 250)


def update_window_size(width, height):
    # Validate width and height then
    Window.size = (width, height)


class MyApp(App):
    def build(self):
        return sm

MyApp().run()
