from functools import partial
from os import path

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from drawer import NavigationDrawer
from request_handler import get_questions, post_answer, get_notifications, post_image, get_image
from variables import files_path


profile = {
    'display_name': 'Amin Etesamian',
    'age': '23',
    'gender': 'male',
    'reputation': '3690'
}
cached_questions = None
cached_notifications = None
question = None
user = {
    'id': 1
}
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

        navigationdrawer = NavigationDrawer()

        side_panel = ProfileScreen()
        navigationdrawer.add_widget(side_panel)
        navigationdrawer.add_widget(root)
        Window.add_widget(navigationdrawer)

    def select_question(self, *args):
        global question
        question = args[0]
        screen_manager.switch_to(QuestionScreen())


class QuestionScreen(Screen):
    answer_text = ''

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

            new_answer_container = RelativeLayout(size_hint=(1, None), size=(Window.width, Window.height / 3))
            answer_input = TextInput(
                size_hint=(None, None),
                size=(Window.width / 2, Window.height / 4),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            answer_input.bind(text=self.set_answer_text)
            submit_button = Button(
                text='Submit',
                size_hint=(None, None),
                size=(Window.width / 10, Window.height / 10),
                pos_hint={'center_x': 0.9, 'center_y': 0.3}
            )
            new_answer_container.add_widget(answer_input)
            new_answer_container.add_widget(submit_button)
            submit_button.bind(on_press=partial(self.submit_answer, user['id'], question['id']))
            body.add_widget(new_answer_container)

            root.add_widget(body)
            self.add_widget(root)

    def submit_answer(self, account_id, question_id, button):
        post_answer(self.answer_text, account_id, question_id)

    def set_answer_text(self, instance, value):
        self.answer_text = value


class NotificationScreen(Screen):
    def __init__(self):
        super(NotificationScreen, self).__init__()

        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        body = GridLayout(cols=1, spacing=2, size_hint_y=None)
        body.bind(minimum_height=body.setter('height'))
        global cached_notifications
        if not cached_notifications:
            cached_notifications = get_notifications(user['id'])
        for n in cached_notifications:
            container = RelativeLayout(size_hint=(1, None), size=(Window.width, Window.height / 10))
            content = Label(text='[ref=%s]%s[/ref]' % (n['content'], n['content']), markup=True)
            content.bind(on_ref_press=partial(self.select_notification, n))
            container.add_widget(content)
            container.add_widget(Label(text=n['creation_time'], pos_hint={'center_x': 0.8, 'center_y': 0.1}))
            body.add_widget(container)
        root.add_widget(body)
        self.add_widget(root)

    def select_notification(self, *args):
        global question
        question = args[0]
        screen_manager.switch_to(QuestionScreen())


class SignUp(Screen):
    def __init__(self):
        super(SignUp, self).__init__()
        root = BoxLayout(orientation='vertical')
        header = GridLayout(cols=1, size_hint=(1, .1))
        with header.canvas.before:
            Color(.28, .40, .28, .8)
            header.rect = Rectangle(size=header.size, pos=header.pos)
        header.bind(pos=self.update_rect, size=self.update_rect)
        header.add_widget(Label(text='Question'))
        body = GridLayout(cols=1, spacing=2, size_hint=(1, .9))
        body.bind(minimum_height=body.setter('height'))
        with body.canvas.before:
            Color(.65, .72, .66, .8)
            body.rect = Rectangle(size=body.size, pos=body.pos)
        body.bind(pos=self.update_rect, size=self.update_rect)
        container = RelativeLayout()
        display_name = Label(text='Sign Up', pos_hint={'center_x': 0.5, 'center_y': 0.9})
        container.add_widget(display_name)
        container.add_widget(TextInput(
            hint_text='User Name',
            size_hint=(None, None),
            size=(Window.width / 5, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        ))
        container.add_widget(TextInput(
            hint_text='Display Name',
            size_hint=(None, None),
            size=(Window.width / 5, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        ))
        container.add_widget(TextInput(
            hint_text='Password',
            size_hint=(None, None),
            size=(Window.width / 5, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            password=True
        ))
        container.add_widget(TextInput(
            hint_text='Bio',
            size_hint=(None, None),
            size=(Window.width / 5, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        ))
        body.add_widget(container)
        root.add_widget(header)
        root.add_widget(body)
        self.add_widget(root)

    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size


class UserScreen(Screen):
    def __init__(self):
        super(UserScreen, self).__init__()
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        body = GridLayout(cols=1, spacing=2, size_hint_y=None)
        body.bind(minimum_height=body.setter('height'))

        container = RelativeLayout(size_hint=(1, None), size=(Window.width, Window.height / 3))
        display_name = Label(text=profile['display_name'])
        container.add_widget(display_name)
        container.add_widget(Label(text=profile['age'], pos_hint={'center_x': 0.1, 'center_y': 0.5}))
        container.add_widget(Label(text=profile['gender'], pos_hint={'center_x': 0.8, 'center_y': 0.2}))
        container.add_widget(Label(text=profile['reputation'], pos_hint={'center_x': 0.8, 'center_y': 0.1}))
        body.add_widget(container)
        root.add_widget(body)
        self.add_widget(root)


class ProfileScreen(Screen):

    def __init__(self):
        super(ProfileScreen, self).__init__()
        body = GridLayout(cols=1, spacing=2, size_hint=(1, None), size=(Window.width, Window.height))
        body.bind(minimum_height=body.setter('height'))
        container = RelativeLayout()
        get_image(user['id'])
        img_src = '%s/%s.jpg' % (files_path, user['id'])
        profile_picture = Image(
            source=img_src,
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            size_hint=(1, None),
            size=(Window.width / 5, Window.height / 5)
        )
        container.add_widget(profile_picture)
        display_name = Label(text=profile['display_name'], pos_hint={'center_x': 0.5, 'center_y': 0.4})
        container.add_widget(display_name)
        container.add_widget(Label(text=profile['age'], pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size=dp(20)))
        container.add_widget(Label(text=profile['gender'], pos_hint={'center_x': 0.5, 'center_y': 0.2}))
        container.add_widget(Label(text=profile['reputation'], pos_hint={'center_x': 0.5, 'center_y': 0.1}))
        body.add_widget(container)
        # a = FileChooserIconView()
        # a.filters = ['*.png', '*.jpg', '*.jpeg']
        # a.bind(on_submit=self.choose_file)
        # close = Button(size_hint=(None, None), size=(50, 50))
        # close.bind(on_press=partial(self.close_filechooser, a))
        # # self.add_widget(a)
        self.add_widget(body)

    def choose_file(self, *args):
        post_image(user['id'], args[1][0])

    def close_filechooser(self, *args):
        self.remove_widget(args[0])


class CommunityApp(App):

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def build(self):
        screen_manager.add_widget(SignUp())
        return screen_manager


if __name__ == '__main__':
    CommunityApp().run()
