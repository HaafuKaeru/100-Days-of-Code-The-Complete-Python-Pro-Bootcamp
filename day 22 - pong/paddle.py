from turtle import Turtle


class Paddle(Turtle):

    def __init__(self, position: str):
        super().__init__('square')
        self.color('white')
        self.penup()
        self.shapesize(stretch_wid=5, stretch_len=1)  # 20 x 100
        # self.speed('fastest')
        self.setup(position)

    def setup(self, position: str):
        if position == 'right':
            self.goto(x=350, y=0)
        if position == 'left':
            self.goto(x=-350, y=0)

    def move_up(self):
        new_y = self.ycor() + 20
        if new_y < 245:
            self.sety(new_y)

    def move_down(self):
        new_y = self.ycor() - 20
        if new_y > -240:
            self.sety(new_y)
