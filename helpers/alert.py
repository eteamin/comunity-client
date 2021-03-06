from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window


class Alert(Popup):

    def __init__(self, title, text, button_text, action=None, *args):
        super(Alert, self).__init__()
        self.action = action
        content = AnchorLayout(anchor_x='center', anchor_y='bottom')
        content.add_widget(
            Label(text=text, halign='left', valign='top')
        )
        ok_button = Button(text=button_text, size_hint=(None, None), size=(Window.width / 3, Window.height / 15))
        content.add_widget(ok_button)

        self.popup = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(Window.width / 1.1, Window.height / 3),
            opacity=0.7,
            auto_dismiss=False
        )
        if not action:
            ok_button.bind(on_press=self.popup.dismiss)
        else:
            ok_button.bind(on_press=self._act)

        self.popup.open()

    def _act(self, *args):
        self.popup.dismiss()
        self.action()
