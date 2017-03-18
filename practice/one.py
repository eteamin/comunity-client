from kivy.app import App
from kivy.uix.widget import Widget

import websocket

class Main(Widget):
    pass


class MyApp(App):
    def build(self):
        return Main()

MyApp().run()
