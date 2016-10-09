from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class MyWidget(FloatLayout):
    def __init__(self, *args):
        super(MyWidget, self).__init__()

        self.add_widget(Label(text="Hello", size_hint=(None, None), pos_hint={'center_x':0.4, 'center_y':0.5}))
        self.add_widget(TextInput(text="MyText", multiline=False, size_hint=(0.1,0.05), pos_hint={'center_x':0.5, 'center_y':0.5}))


class ex(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    ex().run()