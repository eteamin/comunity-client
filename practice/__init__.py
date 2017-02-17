from functools import partial

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


class Text(TextInput):
    def __init__(self):
        super(Text, self).__init__()
        self.size_hint = None, None
        self.size = 350, 50
        self.background_color = [1, 1, 1]
        self.moved_up = False

    def on_touch_down(self, touch):
        super(Text, self).on_touch_down(touch)
        if self.collide_point(* touch.pos):
            print "text is touched"
            if self.moved_up is False:
                self.pos = [self.pos[0], self.pos[1] + 350]
                self.moved_up = True
        print self.focus


class MyApp(App):

    def build(self):
        return Text()


if __name__ == '__main__':
    MyApp().run()
