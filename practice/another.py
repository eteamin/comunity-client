from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty


class MyWidget(RelativeLayout):

    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        Builder.load_file('test.kv')
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='MainScreen'))
        self.add_widget(sm)


class MainScreen(Screen):
    lineX = 395 / 2
    lineY = 405 / 2
    circleRad = 400 / 2
    val = NumericProperty(2500)

    def on_touch_down(self, touch):
        # left
        if 50 <= touch.x <= 75 and 195 <= touch.y <= 210:
            self.val = 2500
            print self.val

        # right
        elif 320 <= touch.x <= 350 and 200 <= touch.y <= 215:
            self.val = 7500
            print self.val

from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')

class MyApp(App):

    def build(self):
        return MyWidget()

if __name__ == '__main__':
    MyApp().run()