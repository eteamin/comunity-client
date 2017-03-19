from kivy.app import App
from kivy.uix.widget import Widget


class Main(Widget):
    pass


class MyApp(App):
    def build(self):
        return Main()

MyApp().run()
