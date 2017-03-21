from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App


class CAP(BoxLayout):
    def __init__(self):
        super(CAP, self).__init__()
        box = BoxLayout(background_color=(0, 255, 0, 0.8))

        closer = Button(text="Close", pos_hint={'x': 6, 'center_y': 0.04},
                        size_hint=(0.1, 0.1), background_color=(0, 0, 255, 0.7))
        box.add_widget(closer)

        box.add_widget(Label(text="", index=6))

        p = Popup(title="", content=box, size=(25,
                                               25))
        p.background_color = (0, 0, 255, 0.9)

        closer.bind(on_press=p.dismiss)
        p.open()
        self.add_widget(box)


class MyApp(App):
    def build(self):
        return BoxLayout()

MyApp().run()
