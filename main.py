from functools import partial
from os import path
import json
from Queue import Queue, Empty

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.metrics import dp
from kivy.graphics.texture import Texture
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock

from drawer import NavigationDrawer
from request_handler import *
from helpers import normalize_tags, tell_time_ago, find_step, Alert, valid_email, valid_password, valid_username

resps = Queue()

me = None
user_id = None
question_id = None
tags = None
EVENT_INTERVAL_RATE = 0.1
progress_bar = ProgressBar(max=100)

texture_size = (3, 3)
canvas_size = (Window.width * 10, Window.height * 10)
canvas_x_revert_point = Window.width * 8
canvas_y_revert_point = Window.height * 6
x_step = find_step(Window.width)
y_step = find_step(Window.height)
canvas_move_direction = 'to_left'

config_file = path.abspath(path.join(path.dirname(__file__), 'configuration.json'))
logo_font_path = path.abspath(path.join(path.dirname(__file__), 'fonts', 'free_bsc.ttf'))

screen_manager = ScreenManager(transition=NoTransition())
color = (0.9, 0.9, 0.9, 0.5)


# noinspection PyUnusedLocal
def update_rect(instance, value):
    instance.rect.pos = instance.pos
    instance.rect.size = instance.size


class MainScreen(Screen):

    def __init__(self, name):
        super(MainScreen, self).__init__()
        self.name = name
        self.box_container = BoxLayout(orientation='vertical')

        self.header = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(Window.width, Window.height * .1))
        with self.header.canvas.before:
            Color(0.298, 0.407, 0.843, 1)
            self.header.rect = Rectangle(size=self.header.size, pos=self.header.pos)
        self.header.bind(pos=update_rect, size=update_rect)
        self.toggle_button = AsyncImage(
            size_hint=(None, None),
            size=(self.header.width / 15, self.header.height),
            source='back.png',
            padding=(100, 100),
        )
        self.header.add_widget(self.toggle_button)
        self.header.add_widget(Label(text='Questions'))

        # self.nav_bar = GridLayout(cols=3, size_hint=(1, None), size=(Window.width, Window.height * .05))
        # with self.nav_bar.canvas.before:
        #     Color(.9, .9, .9, .8)
        #     self.nav_bar.rect = Rectangle(size=self.nav_bar.size, pos=self.nav_bar.pos)
        # self.nav_bar.bind(pos=update_rect, size=update_rect)
        #
        # ask_question_label = Label(text='[ref=Ask a Question]Ask a Question[/ref]', markup=True)
        # ask_question_label.bind(on_ref_press=partial(switch_to_screen, NewQuestionScreen, 'new_question'))
        # self.nav_bar.add_widget(ask_question_label)
        # need_help_label = Label(text='[ref=Need Help?]Need Help?[/ref]', markup=True)
        # # need_help_label.bind(on_ref_press=partial(switch_to_screen, MainScreen))
        # self.nav_bar.add_widget(need_help_label)

        self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.9))
        self.body = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.body.bind(minimum_height=self.body.setter('height'))

        with self.body.canvas.before:
            Color(.65, .72, .66, .8)
            self.body.rect = Rectangle(size=(Window.width, Window.height), pos=self.body.pos)
        self.body.bind(pos=update_rect, size=update_rect)

        self.event_scheduled = True
        self.event = Clock.schedule_interval(partial(async_await_resp, self), EVENT_INTERVAL_RATE)
        self.scroll_view.add_widget(self.body)

        self.box_container.add_widget(self.header)
        # self.box_container.add_widget(self.nav_bar)
        self.box_container.add_widget(self.scroll_view)
        self.navigation_drawer = NavigationDrawer()
        self.navigation_drawer.anim_type = 'slide_above_anim'
        side_panel = SidePanel()
        self.navigation_drawer.add_widget(side_panel)
        self.navigation_drawer.add_widget(self.box_container)
        Window.add_widget(self.navigation_drawer)
        Clock.schedule_once(
            partial(insert_progress_bar, Window)) if progress_bar not in self.children else None
        get_questions(resps, me)

    def on_touch_down(self, touch):
        if self.toggle_button.collide_point(*touch.pos):
            self.navigation_drawer.toggle_state()

    def on_resp_ready(self, resp):
        for q in resp['questions']:
            container = RelativeLayout(size_hint=(1, None), size=(Window.width, Window.height / 4))
            with container.canvas.before:
                Line(points=[container.x, container.x, container.width, container.x, 0, 0], width=1)

            title = Label(
                text='[ref=%s]%s[/ref]' % (q['title'], q['title']),
                markup=True,
                pos_hint={'center_x': 0.55, 'center_y': 1},
                color=(0.5, 0.7, 1, 1),
                font_size=dp(15),
                underline=True,
                halign='left',
                valgin='middle',
                outline_width=500
            )
            # print title.size
            # TODO: never ever do this again
            title.text_size = [500, 100]
            title.bind(on_ref_press=partial(self.select_question, q['id']))
            # title.on_touch_down()
            container.add_widget(title)
            container.add_widget(Label(text=str(len(q['votes'])), pos_hint={'center_x': 0.1, 'center_y': 0.65}))
            container.add_widget(Label(text='Votes' if len(q['votes']) > 1 else 'Vote', pos_hint={'center_x': 0.1, 'center_y': 0.55}, font_size=dp(12)))
            container.add_widget(Label(text=str(len(q['views'])), pos_hint={'center_x': 0.1, 'center_y': 0.4}))
            container.add_widget(Label(text='Views' if len(q['views']) > 1 else 'View', pos_hint={'center_x': 0.1, 'center_y': 0.3}, font_size=dp(12)))

            # Handle tags
            tags_container = BoxLayout(
                orientation='horizontal',
                size_hint=(None, None),
                size=(Window.width * .05, Window.height * .05),
                pos_hint={'center_x': 0.2, 'center_y': 0.5}
            )
            for t in q['tags']:
                tag = Button(
                    text=t['name'],
                    size_hint=(None, None),
                    size=(Window.width / 10, Window.height / 20),
                    font_size=dp(10),
                )
                # tag.text_size = tag.size
                tags_container.add_widget(tag)
            container.add_widget(tags_container)
            creation_date = Label(
                text=tell_time_ago(q['creation_date']),
                pos_hint={'center_x': 0.6, 'center_y': 0.39},
                font_size=dp(12),
                halign='left'
            )
            creation_date.text_size = creation_date.size
            container.add_widget(creation_date)
            username = Label(
                text="[ref=%s]%s[/ref]" % (q['accounts']['username'], q['accounts']['username']), markup=True,
                pos_hint={'center_x': 0.8, 'center_y': 0.1},
                font_size=dp(15),
                color=(0, 1, .4, .8)
            )
            username.bind(on_ref_press=partial(self.select_user, q['accounts']['id']))
            container.add_widget(username)
            image = q['accounts']['image']
            user_image = AsyncImage(
                source='back.png' if not image else image,
                pos_hint={'center_x': 0.8, 'center_y': 0.39},
                size_hint=(None, None),
                size=(Window.width / 8, Window.height / 8)
            )
            container.add_widget(user_image)
            self.body.add_widget(container)

    def select_question(self, *args):
        global question_id
        question_id = args[0]
        switch_to_screen(self, QuestionScreen, 'question')

    def select_user(self, *args):
        global user_id
        user_id = args[0]
        switch_to_screen(self, UserScreen, 'user')


class NewQuestionScreen(Screen):
    title_input_text = ''
    question_input_text = ''
    tags_input_text = ''

    def __init__(self, name):
        super(NewQuestionScreen, self).__init__()
        self.name = name
        global tags
        if not tags:
            tags = get_tags()

        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        box_container = BoxLayout(orientation='vertical')

        header = GridLayout(cols=1, size_hint=(1, .05))
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
        ask_question_label.bind(on_ref_press=partial(switch_to_screen, NewQuestionScreen, 'new_question'))
        nav_bar.add_widget(ask_question_label)
        need_help_label = Label(text='[ref=Need Help?]Need Help?[/ref]', markup=True)
        need_help_label.bind(on_ref_press=partial(switch_to_screen, MainScreen, 'main'))
        nav_bar.add_widget(need_help_label)

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

        self.tag_button = Button(
            hint_text='Tags',
            size_hint=(None, None),
            size=(Window.width / 1.3, Window.height / 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.15},
            read_only=True
        )
        self.tag_button.bind(on_press=self.on_tag_selection)
        self.tag_button.bind(text=partial(self.update_input_text, 'tags'))

        container.add_widget(self.tag_button)

        tag_help = Label(
            text='Question tags separated by comma. example: grammar, word meaning',
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        container.add_widget(tag_help)

        body.add_widget(container)

        box_container.add_widget(header)
        box_container.add_widget(nav_bar)
        box_container.add_widget(body)

        scroll_view.add_widget(box_container)

        navigation_drawer = NavigationDrawer()

        side_panel = SidePanel()
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

    # noinspection PyUnusedLocal
    def post_question(self, *args):
        tags = normalize_tags(self.tags_input_text)
        resp = post_question(self.title_input_text, self.question_input_text, int(me['id']), tags=tags)
        if resp:
            screen_manager.switch_to(MainScreen())
        # TODO: Implement handling of possible exceptions

    # noinspection PyUnusedLocal
    def on_tag_selection(self, *args):
        content = BoxLayout()
        if tags:
            for t in tags:
                name = t['name']
                tag = Button(text=name)
                tag.bind(on_press=partial(self.modify_tags_selection, name))
                content.add_widget(tag)
        ok_button = Button(text='OK', size_hint=(None, None), size=(150, 50))
        content.add_widget(ok_button)

        popup = Popup(
            title='',
            content=content,
            size_hint=(None, None),
            size=(350, 350),
            auto_dismiss=True)
        ok_button.bind(on_press=popup.dismiss)
        popup.open()

    def modify_tags_selection(self, *args):
        tag_name = args[0]
        if tag_name not in self.tags_input_text:
            self.tags_input_text += '#%s ' % tag_name
        else:
            self.tags_input_text = self.tags_input_text.replace('#%s ' % tag_name, '')
        self.tag_button.text = self.tags_input_text


class QuestionScreen(Screen):
    answer_text = ''

    def __init__(self, name):
        super(QuestionScreen, self).__init__()
        self.name = name
        print self.name + 'is called'
        if question_id:
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
            ask_question_label.bind(on_ref_press=partial(switch_to_screen, NewQuestionScreen, 'new_question'))
            nav_bar.add_widget(ask_question_label)
            need_help_label = Label(text='[ref=Need Help?]Need Help?[/ref]', markup=True)
            need_help_label.bind(on_ref_press=partial(switch_to_screen, MainScreen, 'main'))
            nav_bar.add_widget(need_help_label)

            scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.9))
            body = GridLayout(cols=1, spacing=2, size_hint_y=None)
            body.bind(minimum_height=body.setter('height'))

            with body.canvas.before:
                Color(.65, .72, .66, .8)
                body.rect = Rectangle(size=(Window.width, Window.height / 4), pos=body.pos)
            body.bind(pos=update_rect, size=update_rect)
            
            question = get_question(question_id, me['id'])
            
            question_container = RelativeLayout(size_hint=(1, None), size=(Window.width, Window.height / 3))
            title = Label(
                text=question['title'],
                halign='left',
                markup=True,
                pos_hint={'center_x': 0.4, 'center_y': 0.8}
            )
            question_container.add_widget(title)
            # question_container.add_widget(Label(text=question['votes'], pos_hint={'center_x': 0.1, 'center_y': 0.5}))
            # container.add_widget(Label(text=q['account']['display_name'], pos_hint={'center_x': 0.8, 'center_y': 0.2}))
            question_container.add_widget(Label(text=question['creation_date'], pos_hint={'center_x': 0.8, 'center_y': 0.1}))
            body.add_widget(question_container)

            for a in get_children(question['id']):
                container = RelativeLayout(size_hint=(1, None), size=(Window.width, Window.height / 4))
                container.add_widget(Label(text=a['description']))
                for c in get_children(a['id']):
                    pass
                body.add_widget(container)

            self.answer_input = TextInput(
                hint_text='Write your answer',
                size_hint=(None, None),
                size=(Window.width, Window.height / 2),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
            )
            self.answer_input.bind(text=partial(self.update_input_text, 'answer'))
            body.add_widget(self.answer_input)

            submit = Button(
                text='Submit',
                size_hint=(None, None),
                size=(Window.width, Window.height / 20),
                pos_hint={'center_x': 0.5, 'center_y': 0.05},
                background_normal='',
                background_color=(.28, .40, .28, 1)
            )
            submit.bind(on_press=self.submit_answer)
            body.add_widget(submit)

            scroll_view.add_widget(body)

            box_container.add_widget(header)
            box_container.add_widget(nav_bar)
            box_container.add_widget(scroll_view)

            navigation_drawer = NavigationDrawer()

            side_panel = SidePanel()
            navigation_drawer.add_widget(side_panel)
            navigation_drawer.add_widget(box_container)
            Window.add_widget(navigation_drawer)

    # noinspection PyUnusedLocal
    def submit_answer(self, *args):
        resp = post_answer(self.answer_text, me['id'], question_id)
        if resp:
            switch_to_screen(QuestionScreen)
        # TODO: implement exception handling

    def update_input_text(self, *args):
        referer = args[0]
        value = args[2]
        # args[0] is the referer and args[2] is the value of the textbox
        if referer == 'answer':
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

    @staticmethod
    def select_notification(self, *args):
        global question
        question = args[0]
        screen_manager.switch_to(QuestionScreen())


class SignUp(Screen):
    user_name_text = ''
    email_text = ''
    password_text = ''
    repeat_pass_text = ''

    def __init__(self, name):
        self.name = name
        super(SignUp, self).__init__()
        root = BoxLayout(orientation='vertical')

        self.texture = Texture.create(size=texture_size, colorfmt="rgb")
        pixels = bytes([int(v * 255) for v in (0.0, 0.0, 0.0)])
        buf = ''.join(pixels)
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

        body = GridLayout(cols=1, spacing=2, size_hint=(1, 1))
        body.bind(minimum_height=body.setter('height'))
        with body.canvas.before:
            self.canvas_size = canvas_size
            self.rect = Rectangle(pos=self.pos, size=self.canvas_size, texture=self.texture)
        self.canvas_event = Clock.schedule_interval(partial(update_canvas, self.rect), EVENT_INTERVAL_RATE)
        container = RelativeLayout()
        title = Label(
            text="Community",
            font_name=logo_font_path,
            font_size=dp(42),
            pos_hint={'center_x': 0.5, 'center_y': 0.85},
        )
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
            hint_text='Username',
            hint_text_color=(1, 1, 1, 1),
            foreground_color=(1, 1, 1, 1),
            padding_x=[20, 0],
            size_hint=(None, None),
            size=(Window.width / 1.2, Window.height / 12),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            opacity=0.4
        )
        user_name_input.padding_y = [user_name_input.size[1] / 3, 0]
        user_name_input.bind(text=partial(self.update_input_text, 'user_name'))
        container.add_widget(user_name_input)

        email_input = TextInput(
            hint_text='Email Address',
            hint_text_color=[1, 1, 1, 1],
            foreground_color=(1, 1, 1, 1),
            padding_x=[20, 0],
            size_hint=(None, None),
            size=(Window.width / 1.2, Window.height / 12),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            opacity=0.4
        )
        email_input.padding_y = [email_input.size[1] / 3, 0]
        email_input.bind(text=partial(self.update_input_text, 'email'))
        container.add_widget(email_input)

        password_input = TextInput(
            hint_text='Password',
            hint_text_color=[1, 1, 1, 1],
            foreground_color=(1, 1, 1, 1),
            padding_x=[20, 0],
            size_hint=(None, None),
            size=(Window.width / 1.2, Window.height / 12),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            password=True,
            opacity=0.4
        )
        password_input.padding_y = [password_input.size[1] / 3, 0]
        password_input.bind(text=partial(self.update_input_text, 'password'))
        container.add_widget(password_input)

        self.repeat_password_input = TextInput(
            hint_text='Repeat Password',
            hint_text_color=[1, 1, 1, 1],
            foreground_color=(1, 1, 1, 1),
            padding_x=[20, 0],
            size_hint=(None, None),
            size=(Window.width / 1.2, Window.height / 12),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            password=True,
            opacity=0.4
        )
        self.repeat_password_input.bind(focus=self.on_repeat_password_focus)
        self.repeat_password_input.padding_y = [self.repeat_password_input.size[1] / 3, 0]
        self.repeat_password_input.bind(text=partial(self.update_input_text, 'repeat_password'))
        container.add_widget(self.repeat_password_input)

        register_button = Button(
            text='Register',
            size_hint=(None, None),
            size=(Window.width / 1.2, Window.height / 12),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            background_normal='',
            background_color=(1, 1, 1, 0.6),
            opacity=0.8,
            color=(1, 1, 1, 1)
        )
        register_trigger = Clock.create_trigger(self.register)
        register_button.bind(on_press=partial(register_trigger))
        container.add_widget(register_button)
        self.event_scheduled = False

        login_button = Button(
            text='Already have an account? [b]Sign In![/b]', markup=True,
            size_hint=(None, None),
            size=(Window.width, Window.height / 10),
            pos_hint={'center_x': 0.5, 'center_y': 0.05},
            background_normal='',
            background_color=(1, 1, 1, 0.3),
            opacity=0.8,
            color=(1, 1, 1, 1)
        )
        login_button.bind(on_press=partial(switch_to_screen, self, SignIn, 'sign_in'))
        container.add_widget(login_button)

        body.add_widget(container)
        root.add_widget(body)
        self.add_widget(root)
        self.has_moved = False
        Window.clearcolor = (.9, .9, .9, 1)

    def update_input_text(self, *args):
        referer = args[0]
        value = args[2]
        # args[0] is the referer and args[2] is the value of the textbox
        if referer == 'user_name':
            self.user_name_text = value
        elif referer == 'password':
            self.password_text = value
        elif referer == 'email':
            self.email_text = value
        else:
            self.repeat_pass_text = value

    # noinspection PyUnusedLocal
    def register(self, *args):
        if not self.event_scheduled:
            if self._register():
                self.event_scheduled = True
                Clock.schedule_once(partial(insert_progress_bar, self)) if progress_bar not in self.children else None
                self.event = Clock.schedule_interval(partial(async_await_resp, self), EVENT_INTERVAL_RATE)

    # noinspection PyUnusedLocal
    def _register(self, *args):
        self.validate_registration_inputs()
        if self.validation_message == '':
            register(resps, self.user_name_text, self.password_text, self.email_text)
            return True
        else:
            Alert('Hint', self.validation_message)

    def on_resp_ready(self, resp):
        switch_to_screen(self, SignIn, 'sign_in')

    def validate_registration_inputs(self):
        self.validation_message = ''
        if not valid_username(self.user_name_text):
            self.validation_message = 'Invalid Username!'
        elif not valid_password(self.password_text, self.repeat_pass_text):
            self.validation_message = 'Password must be at least 8 characters!'
        elif not valid_email(self.email_text):
            self.validation_message = 'Invalid Email!'

    def on_repeat_password_focus(self, instance, value):
        if value and self.has_moved is False:
            self.pos = self.pos[0], self.pos[1] + Window.height / 5
            self.has_moved = True
        elif not value and self.has_moved is True:
            self.pos = self.pos[0], self.pos[1] - Window.height / 5
            self.has_moved = False


class SignIn(Screen):
    user_name_text = ''
    password_text = ''

    def __init__(self, name):
        self.name = name
        super(SignIn, self).__init__()
        root = BoxLayout(orientation='vertical')

        self.texture = Texture.create(size=texture_size, colorfmt="rgb")
        pixels = bytes([int(v * 255) for v in (0.0, 0.0, 0.0)])
        buf = ''.join(pixels)
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.canvas_move_direction = 'to_left'

        body = GridLayout(cols=1, spacing=2, size_hint=(1, 1))
        body.bind(minimum_height=body.setter('height'))
        with body.canvas.before:
            self.canvas_size = canvas_size
            self.rect = Rectangle(pos=self.pos, size=self.canvas_size, texture=self.texture)
            self.event = Clock.schedule_interval(partial(update_canvas, self.rect), EVENT_INTERVAL_RATE)

        container = RelativeLayout()
        title = Label(
            text="Community",
            font_name=logo_font_path,
            font_size=dp(42),
            pos_hint={'center_x': 0.5, 'center_y': 0.85},
        )
        container.add_widget(title)

        user_name_input = TextInput(
            hint_text='Username',
            hint_text_color=(1, 1, 1, 1),
            foreground_color=(1, 1, 1, 1),
            padding_x=[20, 0],
            size_hint=(None, None),
            size=(Window.width / 1.2, Window.height / 12),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            opacity=0.4
        )
        user_name_input.padding_y = [user_name_input.size[1] / 3, 0]
        user_name_input.bind(text=partial(self.update_input_text, 'user_name'))
        container.add_widget(user_name_input)

        password_input = TextInput(
            hint_text='Password',
            hint_text_color=[1, 1, 1, 1],
            padding_x=[20, 0],
            size_hint=(None, None),
            size=(Window.width / 1.2, Window.height / 12),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            password=True,
            opacity=0.4
        )
        password_input.padding_y = [password_input.size[1] / 3, 0]
        password_input.bind(text=partial(self.update_input_text, 'password'))
        container.add_widget(password_input)

        sign_in_button = Button(
            text='Login',
            size_hint=(None, None),
            size=(Window.width / 1.2, Window.height / 12),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_normal='',
            background_color=(1, 1, 1, 0.6),
            opacity=0.8,
            color=(1, 1, 1, 1)
        )
        sign_in_button.bind(on_press=self.sign_in)
        container.add_widget(sign_in_button)
        self.event_scheduled = False
        register_button = Button(
            text="Don't have an account yet? [b]Sign Up![/b]", markup=True,
            size_hint=(None, None),
            size=(Window.width, Window.height / 10),
            pos_hint={'center_x': 0.5, 'center_y': 0.05},
            background_normal='',
            background_color=(1, 1, 1, 0.3),
            opacity=0.8,
            color=(1, 1, 1, 1)
        )
        register_button.bind(on_press=partial(switch_to_screen, self, SignUp, 'sign_up'))
        container.add_widget(register_button)

        body.add_widget(container)
        root.add_widget(body)
        self.add_widget(root)

    # noinspection PyUnusedLocal
    def sign_in(self, *args):
        if not self.event_scheduled:
            if self._sign_in():
                self.event_scheduled = True
                Clock.schedule_once(partial(insert_progress_bar, self)) if progress_bar not in self.children else None
                self.event = Clock.schedule_interval(partial(async_await_resp, self), EVENT_INTERVAL_RATE)

    # noinspection PyUnusedLocal
    def _sign_in(self, *args):
        # print 'doing registration'
        self.validate_login_inputs()
        if self.validation_message == '':
            login(resps, self.user_name_text, self.password_text)
            return True
        else:
            Alert('Hint', self.validation_message)

    def on_resp_ready(self, resp):
        write_config(resp)
        switch_to_screen(self, MainScreen, 'main')

    def validate_login_inputs(self):
        self.validation_message = ''
        if not valid_username(self.user_name_text):
            self.validation_message = 'Invalid Username!'
        elif not valid_password(self.password_text, self.password_text):
            self.validation_message = 'Password must be at least 8 characters!'

    def update_input_text(self, *args):
        # args[0] is the referer and args[2] is the value of the textbox
        if args[0] == 'user_name':
            self.user_name_text = args[2]
        else:
            self.password_text = args[2]


class UserScreen(Screen):
    def __init__(self):
        super(UserScreen, self).__init__()
        global user_id
        if user_id:
            user = get_user(user_id)
            scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
            box_container = BoxLayout(orientation='vertical')

            header = GridLayout(cols=1, size_hint=(1, .05))
            with header.canvas.before:
                Color(.28, .40, .28, .8)
                header.rect = Rectangle(size=header.size, pos=header.pos)
            header.bind(pos=update_rect, size=update_rect)
            header.add_widget(Label(text='%s Profile' % user['username']))

            body = GridLayout(cols=1, spacing=2, size_hint=(1, .90))
            body.bind(minimum_height=body.setter('height'))

            with body.canvas.before:
                Color(.65, .72, .66, .8)
                body.rect = Rectangle(size=(Window.width, Window.height / 4), pos=body.pos)
            body.bind(pos=update_rect, size=update_rect)

            container = RelativeLayout()

            body.add_widget(container)

            box_container.add_widget(header)
            box_container.add_widget(body)

            scroll_view.add_widget(box_container)

            navigation_drawer = NavigationDrawer()

            side_panel = SidePanel()
            navigation_drawer.add_widget(side_panel)
            navigation_drawer.add_widget(scroll_view)
            Window.add_widget(navigation_drawer)


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


class SidePanel(Screen):

    def __init__(self):
        super(SidePanel, self).__init__()
        if me:
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
            # close.bind(on_press=partial(self.close_file_chooser, a))
            # # self.add_widget(a)
            self.add_widget(body)

    def choose_file(self, *args):
        post_image(me['id'], args[1][0])

    def close_file_chooser(self, *args):
        self.remove_widget(args[0])


def switch_to_screen(*args):
    referer = args[0]
    s_obj = args[1]
    s_name = args[2]
    if issubclass(s_obj, Screen):
        screen_manager.add_widget(s_obj(name=s_name)) if s_name not in screen_manager.screen_names else None
        screen_manager.current = s_name
        if referer:
            screen_manager.real_remove_widget(referer)
    print screen_manager.children


# noinspection PyUnusedLocal
def update_canvas(rect, dt):
    x = rect.pos[0]
    y = rect.pos[1]
    _update_move_direction(rect, x, y)


def _update_move_direction(rect, x, y):
    global canvas_move_direction
    if x == -canvas_x_revert_point and y == 0 and canvas_move_direction == 'to_up':
        canvas_move_direction = 'to_right'
    elif x == -canvas_x_revert_point and y == 0:
        canvas_move_direction = 'to_down'
    elif x == -canvas_x_revert_point and y == -canvas_y_revert_point:
        canvas_move_direction = 'to_up'
    elif x == 0 and y == 0:
        canvas_move_direction = 'to_left'
    _move_canvas(rect, x, y)


def _move_canvas(rect, x, y):
    direction = canvas_move_direction
    if direction == 'to_left':
        rect.pos = x - x_step, y
    elif direction == 'to_right':
        rect.pos = x + x_step, y
    elif direction == 'to_up':
        rect.pos = x, y + y_step
    elif direction == 'to_down':
        rect.pos = x, y - y_step


# noinspection PyUnusedLocal
def insert_progress_bar(widget, *args):
    widget.add_widget(progress_bar)
    progress_bar.pos_hint = {'center_x': 0.5, 'center_y': 0.996}
    progress_bar.value = 0


# noinspection PyUnusedLocal
def async_await_resp(widget, dt):
    try:
        resp = resps.get(timeout=EVENT_INTERVAL_RATE / 2)
        reset(widget)
        if 'detail' in resp:  # Means an error occurred
            Alert('Ops!', resp['detail'])
        else:
            widget.on_resp_ready(resp)
    except Empty as QueueEmpty:
        progress_bar.value += 2


def reset(widget):
    Clock.unschedule(widget.event)
    if hasattr(widget, 'progress_bar'):
        widget.remove_widget(progress_bar)
    else:
        Window.remove_widget(progress_bar)
    widget.event_scheduled = False
    progress_bar.value = 0


def write_config(c):
    with open(config_file, 'w') as stream:
        data = json.dumps(c)
        stream.write(data)
    _reload_config()


def read_config():
    with open(config_file, 'r') as stream:
        return stream.read()


def _reload_config():
    global me
    me = json.loads(read_config())


class CommunityApp(App):
    def on_start(self):
        global me
        user_info = read_config()
        if user_info:
            me = json.loads(user_info)['user']
            if me and 'id' in me:
                switch_to_screen(None, MainScreen, 'main')
        else:
            switch_to_screen(None, SignUp, 'sign_up')

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
