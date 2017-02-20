from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.clock import Clock

layout = """
<Box>:
    orientation: 'vertical'
    Button:
        id: butt
        text: "hello"
        size_hint: (None, None)
        size: (100, 100)
        on_press: root.change()
    Label:
        id: label_text
        text: root.label_text
"""


class Box(BoxLayout):
    label_text = StringProperty()
    interval = 0.5  # Second
    offset = 0

    def change(self):
        # You ask the clock to update the label's value every self.interval (0.5) second
        self.event = Clock.schedule_interval(self.update_label_text, self.interval)

    def update_label_text(self, dt):
        if self.offset < 10:
            self.label_text = "some_text" + str(self.offset)
            self.offset += 1
        else:
            # Finally ask the clock to forget about the update
            Clock.unschedule(self.event)


class TestApp(App):
    def build(self):
        Builder.load_string(layout)
        return Box()

TestApp().run()