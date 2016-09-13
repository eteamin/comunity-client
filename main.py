from kivy.uix.boxlayout import BoxLayout
from kivy.app import App


class MainPage(BoxLayout):
    def __init__(self):
        super(MainPage, self).__init__()
        self.add_widget(QuestionPage())


class QuestionPage(BoxLayout):
    pass


class NotificationPage(BoxLayout):
    pass


class ProfilePage(BoxLayout):
    pass


class CommunityApp(App):

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def build(self):
        return MainPage()


if __name__ == '__main__':
    CommunityApp().run()
