from functools import partial
from os import path

import yaml
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, ReferenceListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
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
from request_handler import get_questions, post_answer, get_notifications, post_image, get_tags, login, register, \
    post_question, get_answers
from helpers import normalize_tags
from variables import files_path


me = None
profile = None
question = None

config_file = path.abspath(path.join(path.dirname(__file__), 'configuration.yaml'))

screen_manager = ScreenManager(transition=SlideTransition())


def update_rect(instance, value):
    instance.rect.pos = instance.pos
    instance.rect.size = instance.size


# class Header(GridLayout):
#     size_hint = None
#
#     def __init__(self):
#         super(Header, self).__init__()
#
#         with self.canvas.before:
#             Color(.28, .40, .28, .8)
#             self.rect = Rectangle(size=self.size, pos=self.pos)
#
#         self.bind(pos=update_rect, size=update_rect)
#         self.add_widget(Label(text='Question'))


class MainScreen(Screen):
    def __init__(self):
        super(MainScreen, self).__init__()

        box_container = BoxLayout(orientation='vertical')

        header = GridLayout(cols=1, size_hint=(1, None), size=(Window.width, Window.height * .05))
        with header.canvas.before:
            Color(.28, .40, .28, .8)
            header.rect = Rectangle(size=header.size, pos=header.pos)
        header.bind(pos=update_rect, size=update_rect)
        header.add_widget(Label(text='Question'))

        nav_bar = GridLayout(cols=3, size_hint=(1, None), size=(Window.width, Window.height * .05))
        with nav_bar.canvas.before:
            Color(.9, .9, .9, .8)
            nav_bar.rect = Rectangle(size=nav_bar.size, pos=nav_bar.pos)
        nav_bar.bind(pos=update_rect, size=update_rect)

        ask_question_label = Label(text='[ref=Ask a Question]Ask a Question[/ref]', markup=True)
        ask_question_label.bind(on_ref_press=partial(switch_to_screen, NewQuestionScreen))
        nav_bar.add_widget(ask_question_label)
        need_help_label = Label(text='[ref=Need Help?]Need Help?[/ref]', markup=True)
        # need_help_label.bind(on_ref_press=partial(switch_to_screen, MainScreen))
        nav_bar.add_widget(need_help_label)

        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.9))
        body = GridLayout(cols=1, spacing=2, size_hint_y=None)
        body.bind(minimum_height=body.setter('height'))

        with body.canvas.before:
            Color(.65, .72, .66, .8)
            body.rect = Rectangle(size=(Window.width, Window.height / 4), pos=body.pos)
        body.bind(pos=update_rect, size=update_rect)

        for q in get_questions():
            container = RelativeLayout(size_hint=(1, None), size=(Window.width, Window.height / 4))

            title = Label(
                text='[ref=%s]%s[/ref]' % (q['title'], q['title']),
                halign='left',
                markup=True,
                pos_hint={'center_x': 0.4, 'center_y': 0.8}
            )
            title.bind(on_ref_press=partial(switch_to_screen, SignIn))
            container.add_widget(title)
            container.add_widget(Label(text=q['like'], pos_hint={'center_x': 0.1, 'center_y': 0.5}))
            # container.add_widget(Label(text=q['account']['display_name'], pos_hint={'center_x': 0.8, 'center_y': 0.2}))
            container.add_widget(Label(text=q['creation_time'], pos_hint={'center_x': 0.8, 'center_y': 0.1}))
            body.add_widget(container)

        scroll_view.add_widget(body)

        box_container.add_widget(header)
        box_container.add_widget(nav_bar)
        box_container.add_widget(scroll_view)

        # scroll_view.add_widget(grid_container)

        navigation_drawer = NavigationDrawer()

        side_panel = ProfileScreen()
        navigation_drawer.add_widget(side_panel)
        navigation_drawer.add_widget(box_container)
        Window.add_widget(navigation_drawer)

    # def select_question(self, *args):
    #     global question
    #     question = args[0]
    #     switch_to_screen(QuestionScreen)


class NewQuestionScreen(Screen):
    title_input_text = ''
    question_input_text = ''
    tags_input_text = ''

    def __init__(self):
        super(NewQuestionScreen, self).__init__()

        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        box_container = BoxLayout(orientation='vertical')

        header = GridLayout(cols=1, size_hint=(1, .05))
        with header.canvas.before:
            Color(.28, .40, .28, .8)
            header.rect = Rectangle(size=header.size, pos=header.pos)
        header.bind(pos=update_rect, size=update_rect)
        header.add_widget(Label(text='Question'))

        body = GridLayout(cols=1, spacing=2, size_hint=(1, .90))
        body.bind(minimum_height=body.setter('height'))

        with body.canvas.before:
            Color(.65, .72, .66, .8)
            body.rect = Rectangle(size=(Window.width, Window.height / 4), pos=body.pos)
        body.bind(pos=update_rect, size=update_rect)

        container = RelativeLayout()
        title = Label(text='Post Your Question', pos_hint={'center_x': 0.5, 'center_y': 0.9})
        container.add_widget(title)

        self.title_input = TextInput(
            hint_text='Title',
            size_hint=(None, None),
            size=(Window.width / 1.3, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        self.title_input.bind(text=partial(self.update_input_text, 'title'))
        container.add_widget(self.title_input)

        self.question_input = TextInput(
            hint_text='Question',
            size_hint=(None, None),
            size=(Window.width / 1.3, Window.height / 2),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )
        self.question_input.bind(text=partial(self.update_input_text, 'question'))
        container.add_widget(self.question_input)

        sign_in = Button(
            text='Post',
            size_hint=(None, None),
            size=(Window.width / 4, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.05},
            background_normal='',
            background_color=(.28, .40, .28, 1)
        )
        sign_in.bind(on_press=self.post_question)
        container.add_widget(sign_in)

        self.tag_input = TextInput(
            hint_text='Tags',
            size_hint=(None, None),
            size=(Window.width / 1.3, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.15},
        )
        self.tag_input.bind(text=partial(self.update_input_text, 'tag'))

        container.add_widget(self.tag_input)

        tag_help = Label(
            text='Question tags separated by comma. example: grammar, word meaning',
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        container.add_widget(tag_help)

        body.add_widget(container)

        box_container.add_widget(header)
        box_container.add_widget(body)

        scroll_view.add_widget(box_container)

        navigation_drawer = NavigationDrawer()

        side_panel = ProfileScreen()
        navigation_drawer.add_widget(side_panel)
        navigation_drawer.add_widget(scroll_view)
        Window.add_widget(navigation_drawer)

    def update_input_text(self, *args):
        referer = args[0]
        value = args[2]
        # args[0] is the referer and args[2] is the value of the textbox
        if referer == 'title':
            self.title_input_text = value
        elif referer == 'question':
            self.question_input_text = value
        elif referer == 'tag':
            self.tags_input_text = value

    def post_question(self, *args):
        tags = normalize_tags(self.tags_input_text)
        server_resp = post_question(self.title_input_text, self.question_input_text, int(me['id']), tags=tags)
        if server_resp['OK']:
            screen_manager.switch_to(MainScreen())
        # TODO: Implement handling of possible exceptions


class QuestionScreen(Screen):
    answer_text = ''

    def __init__(self):
        super(QuestionScreen, self).__init__()
        if question:
            root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))

            # body = GridLayout(cols=1, spacing=2, size_hint_y=None)
            # body.bind(minimum_height=body.setter('height'))
            #
            # question_container = RelativeLayout(size_hint=(1, None), size=(Window.width, Window.height / 2))
            # question_container.add_widget(Label(text=question['title'], pos_hint={'center_x': 0.1, 'center_y': 0.5}))
            # question_container.add_widget(
            #     Label(text=question['creation_time'], pos_hint={'center_x': 0.8, 'center_y': 0.1})
            # )
            # # question_container.add_widget(
            #     # Label(text=question['account']['display_name'], pos_hint={'center_x': 0.8, 'center_y': 0.2})
            # # )
            # body.add_widget(question_container)
            #
            # for a in get_answers(question['id']):
            #     container = RelativeLayout(size_hint=(1, None), size=(Window.width, Window.height / 3))
            #     container.add_widget(Label(text=a['content'], pos_hint={'center_x': 0.1, 'center_y': 0.5}))
            #     container.add_widget(Label(text=a['like'], pos_hint={'center_x': 0.1, 'center_y': 0.5}))
            #     # container.add_widget(
            #     #     Label(text=a['account']['display_name'], pos_hint={'center_x': 0.8, 'center_y': 0.2})
            #     # )
            #     container.add_widget(Label(text=a['creation_time'], pos_hint={'center_x': 0.8, 'center_y': 0.1}))
            #     body.add_widget(container)
            #
            # new_answer_container = RelativeLayout(size_hint=(1, None), size=(Window.width, Window.height / 3))
            # answer_input = TextInput(
            #     size_hint=(None, None),
            #     size=(Window.width / 2, Window.height / 4),
            #     pos_hint={'center_x': 0.5, 'center_y': 0.5}
            # )
            # answer_input.bind(text=self.update_answer_text)
            # submit_button = Button(
            #     text='Submit',
            #     size_hint=(None, None),
            #     size=(Window.width / 10, Window.height / 10),
            #     pos_hint={'center_x': 0.9, 'center_y': 0.3}
            # )
            # new_answer_container.add_widget(answer_input)
            # new_answer_container.add_widget(submit_button)
            # submit_button.bind(on_press=partial(self.submit_answer, me['id'], question['id']))
            # body.add_widget(new_answer_container)
            #
            # root.add_widget(body)
            # self.add_widget(root)

    def submit_answer(self, account_id, question_id, button):
        post_answer(self.answer_text, account_id, question_id)

    def update_answer_text(self, instance, value):
        self.answer_text = value


class NotificationScreen(Screen):
    def __init__(self):
        super(NotificationScreen, self).__init__()

        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        body = GridLayout(cols=1, spacing=2, size_hint_y=None)
        body.bind(minimum_height=body.setter('height'))
        for n in get_notifications(me['id']):
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
    user_name_text = ''
    password_text = ''
    repeat_pass_text = ''

    def __init__(self):
        super(SignUp, self).__init__()
        root = BoxLayout(orientation='vertical')

        header = GridLayout(cols=1, size_hint=(1, .1))
        with header.canvas.before:
            Color(.28, .40, .28, .8)
            header.rect = Rectangle(size=header.size, pos=header.pos)
        header.bind(pos=update_rect, size=update_rect)
        header.add_widget(Label(text='Question'))

        body = GridLayout(cols=1, spacing=2, size_hint=(1, .9))
        body.bind(minimum_height=body.setter('height'))
        with body.canvas.before:
            Color(.65, .72, .66, .8)
            body.rect = Rectangle(size=body.size, pos=body.pos)
        body.bind(pos=update_rect, size=update_rect)

        container = RelativeLayout()
        title = Label(text='Sign Up', pos_hint={'center_x': 0.5, 'center_y': 0.9})
        container.add_widget(title)

        self.notification_label = Label(
            text='',
            size_hint=(None, None),
            size=(Window.width / 4, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            markup=True
        )
        container.add_widget(self.notification_label)

        user_name_input = TextInput(
            hint_text='User Name',
            size_hint=(None, None),
            size=(Window.width / 4, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        user_name_input.bind(text=partial(self.update_input_text, 'user_name'))
        container.add_widget(user_name_input)

        password_input = TextInput(
            hint_text='Password',
            size_hint=(None, None),
            size=(Window.width / 4, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            password=True
        )
        password_input.bind(text=partial(self.update_input_text, 'password'))
        container.add_widget(password_input)

        repeat_password_input = TextInput(
            hint_text='Repeat Password',
            size_hint=(None, None),
            size=(Window.width / 4, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            password=True
        )
        repeat_password_input.bind(text=partial(self.update_input_text, 'repeat_password'))
        container.add_widget(repeat_password_input)

        register_button = Button(
            text='Register',
            size_hint=(None, None),
            size=(Window.width / 4, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            background_normal='',
            background_color=(.28, .40, .28, 1)
        )
        register_button.bind(on_press=self.register)
        container.add_widget(register_button)

        body.add_widget(container)
        root.add_widget(header)
        root.add_widget(body)
        self.add_widget(root)

    def update_input_text(self, *args):
        referer = args[0]
        value = args[2]
        # args[0] is the referer and args[2] is the value of the textbox
        if referer == 'user_name':
            self.user_name_text = value
        elif referer == 'password':
            self.password_text = value
        else:
            self.repeat_pass_text = value

    def update_notif_text(self, *args):
        self.notification_label.text = '[ref=%s]%s[/ref]' % (args[0], args[0])

    def register(self, *args):
        if register(self.user_name_text, self.password_text)['OK']:
            self.update_notif_text('Registration Complete! Tap Here to Login')
            self.notification_label.bind(on_ref_press=partial(switch_to_screen, SignIn))


def switch_to_screen(*args):
    screen_manager.switch_to(args[0]())


class SignIn(Screen):
    user_name_text = ''
    password_text = ''

    def __init__(self):
        super(SignIn, self).__init__()
        root = BoxLayout(orientation='vertical')
        header = GridLayout(cols=1, size_hint=(1, .1))

        with header.canvas.before:
            Color(.28, .40, .28, .8)
            header.rect = Rectangle(size=header.size, pos=header.pos)

        header.bind(pos=update_rect, size=update_rect)
        header.add_widget(Label(text='Question'))

        body = GridLayout(cols=1, spacing=2, size_hint=(1, .9))
        body.bind(minimum_height=body.setter('height'))

        with body.canvas.before:
            Color(.65, .72, .66, .8)
            body.rect = Rectangle(size=(Window.width, Window.height / 4), pos=body.pos)
        body.bind(pos=update_rect, size=update_rect)

        container = RelativeLayout()
        title = Label(text='Login to your account', pos_hint={'center_x': 0.5, 'center_y': 0.9})
        container.add_widget(title)

        user_name_input = TextInput(
            hint_text='User Name',
            size_hint=(None, None),
            size=(Window.width / 4, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        user_name_input.bind(text=partial(self.update_input_text, 'user_name'))
        container.add_widget(user_name_input)

        password_input = TextInput(
            hint_text='Password',
            size_hint=(None, None),
            size=(Window.width / 4, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            password=True
        )
        password_input.bind(text=partial(self.update_input_text, 'password'))
        container.add_widget(password_input)

        sign_in = Button(
            text='Login',
            size_hint=(None, None),
            size=(Window.width / 4, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_normal='',
            background_color=(.28, .40, .28, 1)
        )
        sign_in.bind(on_press=self.sign_in)
        container.add_widget(sign_in)

        body.add_widget(container)
        root.add_widget(header)
        root.add_widget(body)
        self.add_widget(root)

    def sign_in(self, *args):
        server_resp = login(self.user_name_text, self.password_text)
        if server_resp['OK']:
            with open(config_file, 'w') as stream:
                me = server_resp['Account']
                yaml.dump(me, stream)
            screen_manager.switch_to(MainScreen())
        else:
            # TODO: notify
            pass

    def update_input_text(self, *args):
        # args[0] is the referer and args[2] is the value of the textbox
        if args[0] == 'user_name':
            self.user_name_text = args[2]
        else:
            self.password_text = args[2]


class UserScreen(Screen):
    def __init__(self):
        super(UserScreen, self).__init__()
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        body = GridLayout(cols=1, spacing=2, size_hint_y=None)
        body.bind(minimum_height=body.setter('height'))

        container = RelativeLayout(size_hint=(1, None), size=(Window.width, Window.height / 3))
        user_name = Label(text=me['user_name'])
        container.add_widget(user_name)
        # container.add_widget(Label(text=profile['age'], pos_hint={'center_x': 0.1, 'center_y': 0.5}))
        # container.add_widget(Label(text=profile['gender'], pos_hint={'center_x': 0.8, 'center_y': 0.2}))
        container.add_widget(Label(text=str(me['reputation']), pos_hint={'center_x': 0.8, 'center_y': 0.1}))
        body.add_widget(container)
        root.add_widget(body)
        self.add_widget(root)


class RankScreen(Screen):
    def __init__(self):
        super(RankScreen, self).__init__()
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        box_container = BoxLayout(orientation='vertical')

        header = GridLayout(cols=1, size_hint=(1, .05))
        with header.canvas.before:
            Color(.28, .40, .28, .8)
            header.rect = Rectangle(size=header.size, pos=header.pos)
        header.bind(pos=update_rect, size=update_rect)
        header.add_widget(Label(text='Ranking'))

        body = GridLayout(cols=1, spacing=2, size_hint=(1, .90))
        body.bind(minimum_height=body.setter('height'))

        with body.canvas.before:
            Color(.65, .72, .66, .8)
            body.rect = Rectangle(size=(Window.width, Window.height / 4), pos=body.pos)
        body.bind(pos=update_rect, size=update_rect)

        box_container.add_widget(header)
        box_container.add_widget(body)

        root.add_widget(box_container)
        self.add_widget(root)


class ProfileScreen(Screen):

    def __init__(self):
        super(ProfileScreen, self).__init__()
        if me['id']:
            body = GridLayout(cols=1, spacing=2, size_hint=(1, None), size=(Window.width, Window.height))
            body.bind(minimum_height=body.setter('height'))
            container = RelativeLayout()
            # get_image(user['id'])
            # img_src = '%s/%s.jpg' % (files_path, user['id'])
            # profile_picture = Image(
            #     source=img_src,
            #     pos_hint={'center_x': 0.5, 'center_y': 0.8},
            #     size_hint=(1, None),
            #     size=(Window.width / 5, Window.height / 5)
            # )
            # container.add_widget(profile_picture)
            # display_name = Label(text=me['display_name'], pos_hint={'center_x': 0.5, 'center_y': 0.4})
            # container.add_widget(display_name)
            # container.add_widget(Label(text=me['age'], pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size=dp(20)))
            # container.add_widget(Label(text=me['gender'], pos_hint={'center_x': 0.5, 'center_y': 0.2}))
            container.add_widget(Label(text=str(me['reputation']), pos_hint={'center_x': 0.5, 'center_y': 0.1}))
            body.add_widget(container)
            # a = FileChooserIconView()
            # a.filters = ['*.png', '*.jpg', '*.jpeg']
            # a.bind(on_submit=self.choose_file)
            # close = Button(size_hint=(None, None), size=(50, 50))
            # close.bind(on_press=partial(self.close_filechooser, a))
            # # self.add_widget(a)
            self.add_widget(body)

    def choose_file(self, *args):
        post_image(me['id'], args[1][0])

    def close_filechooser(self, *args):
        self.remove_widget(args[0])


class CommunityApp(App):
    def on_start(self):
        global me
        with open(config_file, 'r') as stream:
            me = yaml.load(stream)
        if me['id']:
            screen_manager.add_widget(MainScreen())
        else:
            screen_manager.add_widget(SignUp())

    def on_pause(self):
        return True

    def on_stop(self):
        pass

    def on_resume(self):
        pass

    def build(self):
        return screen_manager


if __name__ == '__main__':
    CommunityApp().run()
