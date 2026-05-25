from turtle import Turtle, Screen
import random


is_race_on = False
screen = Screen()
screen_size = (500, 400)  # width x height
screen.setup(width=screen_size[0], height=screen_size[1])
user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a colour: ")
colours = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
y_positions = [150, 90, 30, -30, -90, -150]


class TurtleRace(Turtle):
    def __init__(self, colour, starting_y):
        super().__init__(shape='turtle')
        self.color(colour)
        self.starting_y = starting_y
        self.penup()
        self.goto(x=screen_size[0]/2*(-1)+30, y=starting_y)


all_turtles = []
for turtle_index in range(6):
    all_turtles.append(TurtleRace(colours[turtle_index], starting_y=y_positions[turtle_index]))

if user_bet:
    is_race_on = True

while is_race_on:
    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_race_on = False
            winning_colour = turtle.pencolor()
            if winning_colour == user_bet:
                print(f"You won! The {winning_colour} is the winner!")
            else:
                print(f"You lost! The {winning_colour} is the winner!")
        random_distance = random.randint(0, 10)
        turtle.forward(random_distance)

screen.exitonclick()
