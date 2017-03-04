from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.utils import platform

import subprocess


class Main(Widget):
    def __init__(self):
        super(Main, self).__init__()
        if platform == 'linux':
            command = "xdpyinfo  | grep -oP 'dimensions:\s+\K\S+'"
            ps = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = ps.communicate()[0]
            self.add_widget(Label(text=output))


class MyApp(App):
    def build(self):
        return Main()

MyApp().run()
