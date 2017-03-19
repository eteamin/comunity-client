from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App


Builder.load_string("""
<MyListView>:
    ListView:
        Button:
            text: "Close"
            on_release: app.stop()
""")


class MyListView(BoxLayout):
    features = ["A", "B", "C"]


class MyApp(App):
    def build(self):
        return MyListView()

    def on_stop(self):
        return True

if __name__ == '__main__':
    MyApp().run()