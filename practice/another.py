from kivy.app import App
# kivy.require("1.8.0")
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import socket


class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 3
        self.my_socket = socket.socket()
        host = socket.gethostname()
        port = 8585
        self.my_socket.connect((host, port))

        self.add_widget(Label(text='username'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text='Password'))
        self.password = TextInput(multiline=False, password=True)
        self.add_widget(self.password)

        self.submit_button = Button(text='Submit')
        self.submit_button.bind(on_press=self.submit_username)
        self.add_widget(self.submit_button)

    def submit_username(self, *args):
        # Make sure to validate the input before submitting to the server
        self.my_socket.send(bytes(self.username.text))


class SimpleKivy(App):
    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    SimpleKivy().run()
