from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label


class A(RelativeLayout):
    def __init__(self):
        super(A, self).__init__()
        l = Label(
            text="I have a couple of Elastic Load Balancers. I wish to dynamically find the public IP addresses associated with the EC2 Instances which belong to the ELB's Target Group. I used to be able to do it with the previous version of ELB, because the Instance ID's would be listed with each ELB. Now, it seems, they are not. Any clues would be great!",
            halign='left',
            pos_hint={'center_x': 0.4, 'center_y': 0.5},
        )
        l.text_size = self.size[0], self.size[1]
        self.add_widget(l)


class P(App):
    def build(self):
        return A()


P().run()