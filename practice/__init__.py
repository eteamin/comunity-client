from itertools import chain
from random import uniform as u

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.animation import Animation
from colorsys import hsv_to_rgb

EVENT_INTERVAL_RATE = 0.1
step = 25


class MyWidget(Widget):
    def __init__(self, **args):
        super(MyWidget, self).__init__(**args)
        self.texture = Texture.create(size=(4, 3), colorfmt="rgb")
        pixels = bytes([int(v * 255) for v in (0.0, 0.0, 0.0)])
        buf = ''.join(pixels)
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        with self.canvas:
            self.canvas_size = (1000, 1000)
            self.rect = Rectangle(pos=self.pos, size=self.canvas_size, texture=self.texture)
        self.canvas_move_direction = 'to_left'
    #     self.event = Clock.schedule_interval(self.update_texture, EVENT_INTERVAL_RATE)
    #
    # # noinspection PyUnusedLocal
    # def update_texture(self, dt):
    #     x = self.rect.pos[0]
    #     y = self.rect.pos[1]
    #     print x, y
    #     if x == -4200 and y == 0:
    #         self.canvas_move_direction = 'to_down'
    #     elif x == -4200 and y == -1000:
    #         self.canvas_move_direction = 'to_right'
    #     elif x == 0 and y == -1000:
    #         self.canvas_move_direction = 'to_up'
    #     elif x == 0 and y == 0:
    #         self.canvas_move_direction = 'to_left'
    #     self.move_canvas(x, y)
    #
    # def move_canvas(self, x, y):
    #     direction = self.canvas_move_direction
    #     if direction == 'to_left':
    #         self.rect.pos = x - step, y
    #     elif direction == 'to_right':
    #         self.rect.pos = x + step, y
    #     elif direction == 'to_up':
    #         self.rect.pos = x, y + step
    #     elif direction == 'to_down':
    #         self.rect.pos = x, y - step
    #


class TestApp(App):
    def build(self):
        return MyWidget(size=(Window.width, Window.height))


if __name__ == '__main__':
    TestApp().run()
