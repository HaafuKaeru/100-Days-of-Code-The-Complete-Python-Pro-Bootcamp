from turtle import Turtle

from random import randint, choice, uniform


COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10
SPAWN_THRESHOLD = 0.2
COLLISION_BOX = 30


class CarManager:

    def __init__(self):
        self.cars = []
        self.starting_speed = STARTING_MOVE_DISTANCE
        self.cars_in_middle = []

    def spawn_car(self):
        rand_float = uniform(0, 1)
        if rand_float <= SPAWN_THRESHOLD:
            random_position = (280, randint(-280, 280))
            car = Car(starting_pos=random_position, colour=choice(COLORS))
            self.cars.append(car)

    def move_cars(self):
        self.cars_in_middle = []
        for car in self.cars:
            new_xcor = car.xcor() - self.starting_speed
            # remove car if out of screen
            if new_xcor <= -350:
                car.destroy()
                self.cars.remove(car)
            # keep track of cars that are in the middle
            if car.is_in_middle():
                self.cars_in_middle.append(car)
            car.goto(x=new_xcor, y=car.ycor())

    def restart_cars(self):
        for car in self.cars:
            car.destroy()
        self.cars = []
        self.starting_speed += MOVE_INCREMENT


class Car(Turtle):

    def __init__(self, starting_pos, colour):
        super().__init__('square')
        self.penup()
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.color(colour)
        self.goto(starting_pos)

    def destroy(self):
        self.reset()
        self.penup()
        self.hideturtle()

    def is_in_middle(self) -> bool:
        if -COLLISION_BOX <= self.xcor() <= COLLISION_BOX:
            return True
        return False