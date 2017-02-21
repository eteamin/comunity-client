from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window


class Alert(Popup):

    def __init__(self):
        super(Alert, self).__init__()
        content = AnchorLayout(anchor_x='center', anchor_y='bottom')
        content.add_widget(
            Label(text='hello', halign='left', valign='top')
        )
        ok_button = Button(text='Ok', size_hint=(None, None), size=(Window.width / 3, Window.height / 15))
        content.add_widget(ok_button)

        popup = Popup(
            title='bye',
            content=content,
            size_hint=(None, None),
            size=(Window.width / 1.1, Window.height / 3),
            opacity=0.7,
            auto_dismiss=True,
        )
        ok_button.bind(on_press=popup.dismiss)

        popup.open()


class TestApp(App):
    def build(self):
        return Alert()

TestApp().run()