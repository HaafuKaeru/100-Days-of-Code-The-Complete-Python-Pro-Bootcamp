from html.entities import entitydefs
from turtle import Turtle, Screen

from anyio import current_effective_deadline


def draw_square(entity: Turtle):
    for _ in range(4):
        entity.right(90)
        entity.forward(100)


def draw_dashed_line(entity: Turtle):
    for _ in range(15):
        entity.pendown()
        entity.forward(10)
        entity.penup()
        entity.forward(10)


def draw_shapes(entity: Turtle):
    shapes = [3, 4, 5, 6, 7, 8, 9, 10]
    for shape in shapes:
        entity.pencolor(70, 200, shape*20+30)
        for _ in range(shape):
            entity.right(360 / shape)
            entity.forward(100)


def draw_random_walk(entity: Turtle):
    import random
    nice_colours = [
        'steel blue',
        'medium spring green',
        'orange',
        'medium orchid'
    ]
    directions = [
        'right',
        'left',
        'forwards',
        'backwards'
    ]
    step_length = 50
    entity.pensize(20)
    entity.speed(8)

    steps = 100
    for n in range(steps):
        step_colour = nice_colours[n%4]
        entity.color(step_colour)
        entity.pencolor(step_colour)
        direction = random.choice(directions)
        if direction == 'right':
            entity.right(90)
        if direction == 'left':
            entity.left(90)
        if direction == 'backwards':
            entity.left(180)
        entity.forward(step_length)


def draw_spirograph(entity: Turtle):
    from random import randint as rdint
    entity.speed('fastest')
    n_circles = 50
    for _ in range(n_circles):
        entity.color(rdint(0, 255), rdint(0, 255), rdint(0, 255))
        entity.circle(100)
        entity.left(360 / n_circles)


def draw_million_dollar_painting(entity: Turtle):
    import random
    # import colorgram
    # rgb_colors = []
    # colors = colorgram.extract('image.jpg', 30)
    # for color in colors:
    #     rgb_colors.append((color.rgb.r, color.rgb.g, color.rgb.b))
    # print(rgb_colors)
    colours_list = [
        (202, 164, 110), (236, 239, 243), (149, 75, 50), (222, 201, 136), (53, 93, 123), (170, 154, 41), (138, 31, 20),
        (134, 163, 184), (197, 92, 73), (47, 121, 86), (73, 43, 35), (145, 178, 149), (14, 98, 70), (232, 176, 165),
        (160, 142, 158), (54, 45, 50), (101, 75, 77), (183, 205, 171), (36, 60, 74), (19, 86, 89), (82, 148, 129),
        (147, 17, 19), (27, 68, 102), (12, 70, 64), (107, 127, 153), (176, 192, 208), (168, 99, 102)
    ]
    entity.penup()
    entity.hideturtle()
    entity.speed('fastest')
    origin = -250
    entity.setx(origin)
    entity.sety(origin)

    for row in range(10):
        entity.sety(origin + (50*row))
        for col in range(10):
            entity.setx(origin + (50 * col))
            entity.pendown()
            current_colour = random.choice(colours_list)
            entity.pencolor(current_colour)
            entity.fillcolor(current_colour)
            entity.begin_fill()
            entity.circle(10)
            entity.end_fill()
            entity.penup()


def main():
    arrow = Turtle(shape='classic')
    screen = Screen()
    screen.colormode(255)

    draw_million_dollar_painting(arrow)

    screen.exitonclick()


if __name__ == '__main__':
    main()