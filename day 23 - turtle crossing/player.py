from turtle import Turtle


STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10


class Player(Turtle):

    def __init__(self):
        super().__init__('turtle')
        self.penup()
        self.left(90)
        self.reposition()

    def move_up(self):
        self.goto(0, self.ycor() + MOVE_DISTANCE)

    def reposition(self):
        self.goto(STARTING_POSITION)
