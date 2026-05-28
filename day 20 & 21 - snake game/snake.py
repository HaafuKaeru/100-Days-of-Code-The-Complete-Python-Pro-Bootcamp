from turtle import Turtle

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


class Snake:

    def __init__(self):
        self.segments = []
        self._initialise()
        self.head = self.segments[0]
        self.input_blocked = False  # this attribute is needed to stop player from using two keys in succession to make an illegal move (e.g. turning up while going down)

    def _initialise(self):
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position):
        new_segment = Turtle('square')
        new_segment.color('white')
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)

    def extend(self):
        self.add_segment(self.segments[-1].position())

    def move(self):
        for seg_num in range(len(self.segments)-1, 0, -1):
            new_x = self.segments[seg_num-1].xcor()
            new_y = self.segments[seg_num-1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)
        self.input_blocked = False  # allow new input only at each new frame

    def _turn(self, direction: int, opposite_dir: int):
        if self.head.heading() != opposite_dir and not self.input_blocked:
            self.head.setheading(direction)
            self.input_blocked = True

    def up(self):
        self._turn(UP, DOWN)

    def down(self):
        self._turn(DOWN, UP)

    def left(self):
        self._turn(LEFT, RIGHT)

    def right(self):
        self._turn(RIGHT, LEFT)

    def reset_snake(self):
        for segment in self.segments:
            segment.goto(1000, 1000)
        self.__init__()