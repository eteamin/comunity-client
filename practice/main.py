from functools import partial
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window


class MainApp(App):

    def build(self):
        b = Button(text='click to open popup')
        b.bind(on_press=partial(self.view_popup))
        return b

    def view_popup(self, *args):
        data = [1, 2, 3, 4]
        a = PopView(data)
        a.popup.open()


class PopView(Popup):
    items = ''
    def __init__(self, data):
        super(PopView, self).__init__()
        self.data = data
        content = BoxLayout()
        for d in self.data:
            item = Button(text=str(d))
            item.bind(on_press=partial(self.modify_items_selection, item))
            content.add_widget(item)
        ok_button = Button(text='OK', size_hint=(None, None), size=(150, 50))
        content.add_widget(ok_button)

        ok_button = Button(text='Save', size_hint=(None, None), size=(Window.width / 5, Window.height / 15))
        content.add_widget(ok_button)
        self.popup = Popup(
            content=content,
            size_hint=(None, None),
            size=(Window.width / 3, Window.height / 3),
            opacity=0.7,
            auto_dismiss=True,
        )
        ok_button.bind(on_press=self.save_data)

    def modify_items_selection(self, *args):
        item = args[0]
        if item not in self.items:
            self.items += '%s' % item
        else:
            self.items = self.items.replace('%s' % item, '')

    def save_data(self, *args):
        print('Data saved')


if __name__ in ('__main__', '__android__'):
    MainApp().run()