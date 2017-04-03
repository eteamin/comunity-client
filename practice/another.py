from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty
from kivy.lang import Builder

Builder.load_string('''
<MyWidget>:
    CheckBox:
        active: root.odrzuc
        group: "Zone "

    CheckBox:
        active: root.decyduj
        group: "Zone "

''')

class MyWidget(BoxLayout):
    odrzuc = BooleanProperty(False)
    decyduj = BooleanProperty(True)


class MyApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    MyApp().run()