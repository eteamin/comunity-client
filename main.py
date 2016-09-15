from functools import partial

from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView

from request_handler import get_questions
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition


cached_questions = None
question = None
screen_manager = ScreenManager(transition=SlideTransition())


class MainScreen(Screen):
    def __init__(self):
        super(MainScreen, self).__init__()
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        global cached_questions
        if not cached_questions:
            cached_questions = get_questions()

        body = GridLayout(cols=1, spacing=2, size_hint_y=None)
        body.bind(minimum_height=body.setter('height'))

        for q in cached_questions:
            container = RelativeLayout(size_hint=(1, None), size=(Window.width, Window.height / 3))
            title = Label(text='[ref=%s]%s[/ref]' % (q['title'], q['title']), markup=True)
            title.bind(on_ref_press=partial(self.select_question, q))
            container.add_widget(title)
            container.add_widget(Label(text=q['like'], pos_hint={'center_x': 0.1, 'center_y': 0.5}))
            container.add_widget(Label(text=q['account']['display_name'], pos_hint={'center_x': 0.8, 'center_y': 0.2}))
            container.add_widget(Label(text=q['creation_time'], pos_hint={'center_x': 0.8, 'center_y': 0.1}))
            body.add_widget(container)

        root.add_widget(body)
        self.add_widget(root)

    def select_question(self, *args):
        global question
        question = args[0]
        screen_manager.switch_to(QuestionScreen())


class QuestionScreen(Screen):
    def __init__(self):
        super(QuestionScreen, self).__init__()
        if question:
            root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))

            body = GridLayout(cols=1, spacing=2, size_hint_y=None)
            body.bind(minimum_height=body.setter('height'))

            question_container = RelativeLayout(size_hint=(1, None), size=(Window.width, Window.height / 2))
            question_container.add_widget(Label(text=question['title'], pos_hint={'center_x': 0.1, 'center_y': 0.5}))
            question_container.add_widget(
                Label(text=question['creation_time'], pos_hint={'center_x': 0.8, 'center_y': 0.1})
            )
            question_container.add_widget(
                Label(text=question['account']['display_name'], pos_hint={'center_x': 0.8, 'center_y': 0.2})
            )
            body.add_widget(question_container)

            for a in question['answers']:
                container = RelativeLayout(size_hint=(1, None), size=(Window.width, Window.height / 3))
                container.add_widget(Label(text=a['content'], pos_hint={'center_x': 0.1, 'center_y': 0.5}))
                container.add_widget(Label(text=a['like'], pos_hint={'center_x': 0.1, 'center_y': 0.5}))
                container.add_widget(
                    Label(text=a['account']['display_name'], pos_hint={'center_x': 0.8, 'center_y': 0.2})
                )
                container.add_widget(Label(text=a['creation_time'], pos_hint={'center_x': 0.8, 'center_y': 0.1}))
                body.add_widget(container)

            root.add_widget(body)
            self.add_widget(root)


class NotificationScreen(Screen):
    pass


class ProfileScreen(Screen):
    pass


class CommunityApp(App):

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def build(self):
        screen_manager.add_widget(MainScreen())
        return screen_manager


if __name__ == '__main__':
    CommunityApp().run()
