from turtle import Turtle, Screen


arrow = Turtle(shape='arrow')
screen = Screen()
screen.listen()

def move_forwards(steps=20):
    arrow.forward(steps)

def move_backwards(steps=20):
    arrow.backward(steps)

def turn_left(angle=10):
    arrow.left(angle)

def turn_right(angle=10):
    arrow.right(angle)


screen.onkeypress(key='w', fun=move_forwards)
screen.onkeypress(key='a', fun=turn_left)
screen.onkeypress(key='s', fun=move_backwards)
screen.onkeypress(key='d', fun=turn_right)
screen.onkeypress(key='c', fun=screen.resetscreen)


screen.exitonclick()



