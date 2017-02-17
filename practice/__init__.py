from functools import partial

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager

screen_manager = ScreenManager()


class One(Screen):
    def __init__(self, name):
        self.name = name
        super(One, self).__init__()
        a = Label(text='[ref=hi]hi[/ref]', markup=True,)
        a.bind(on_ref_press=partial(switch_to_screen, Two, 'two'))
        self.add_widget(a)


class Two(Screen):
    def __init__(self, name):
        self.name = name
        super(Two, self).__init__()
        a = Label(text='[ref=hi]hi[/ref]', markup=True,)
        a.bind(on_ref_press=partial(switch_to_screen, One, 'one'))
        self.add_widget(a)


def switch_to_screen(*args):
    screen_obj = args[0]
    screen_name = args[1]
    if issubclass(screen_obj, Screen):
        screen_manager.add_widget(screen_obj(name=screen_name)) if screen_name not in screen_manager.screen_names else None
        screen_manager.current = screen_name
    print screen_manager.screen_names


class MyApp(App):
    def build(self):
        screen_manager.add_widget(One(name='one'))
        return screen_manager


if __name__ == '__main__':
    MyApp().run()
