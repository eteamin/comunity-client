from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

layout = """
Box:
    BoxLayout:
        Button:
            id: butt
            text: ""
            on_press: root.change()
        Label:
            id: label_text
"""


class Box(BoxLayout):
    def change(self):
            variable = 0
            while variable < 10:
                text = "Some text " + str(variable)
                variable += 1


class TestApp(App):
    def build(self):
        Builder.load_string(layout)
        return Box()

TestApp().run()