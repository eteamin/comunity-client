from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import BorderImage


class MyApp(App):
    def build(self):
        root = Widget()
        b = Button(center=(200, 200))
        root.add_widget(b)
        with b.canvas.before:
            BorderImage(
                size=(b.width, b.height),
                pos=(b.x, b.y),
                border=(10, 10, 10, 10),
                source='home.png')

        return root


MyApp().run()