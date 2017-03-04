from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label

import subprocess


class Main(Widget):
    def __init__(self):
        super(Main, self).__init__()
        command = "xdpyinfo  | grep -oP 'dimensions:\s+\K\S+'"
        resolution = subprocess.call(command)
        self.add_widget(Label(text=resolution))


class MyApp(App):
    def build(self):
        return Main()

MyApp().run()
