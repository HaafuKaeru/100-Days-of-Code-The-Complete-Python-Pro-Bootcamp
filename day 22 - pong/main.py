from turtle import Screen
from time import sleep

from paddle import Paddle
from ball import Ball
from scoreboard import ScoreBoard


WIDTH = 800
HEIGHT = 600
BGCOLOR = 'blue'


def main():

    screen = Screen()
    screen.setup(width=WIDTH, height=HEIGHT)
    screen.title("Pong")
    screen.bgcolor(BGCOLOR)
    screen.tracer(0)

    right_paddle = Paddle('right')
    left_paddle = Paddle('left')
    ball = Ball()
    scoreboard = ScoreBoard()

    screen.listen()
    screen.onkeypress(right_paddle.move_up, 'Up')
    screen.onkeypress(right_paddle.move_down, 'Down')
    screen.onkeypress(left_paddle.move_up, 'w')
    screen.onkeypress(left_paddle.move_down, 's')

    game_is_on = True
    while game_is_on:
        sleep(ball.move_speed)
        screen.update()
        ball.move()

        # detect collision with wall
        wall = 280
        if ball.ycor() > wall or ball.ycor() < -wall:
            ball.bounce_y()

        # detect collision with paddle
        paddle_x = 320
        paddle_dist = 50
        if ball.distance(right_paddle) < paddle_dist and ball.xcor() > paddle_x or ball.distance(left_paddle) < paddle_dist and ball.xcor() < -paddle_x:
            ball.bounce_x()

        # detect ball going out of bounds
        bound = 390
        if ball.xcor() > bound:  # left point
            ball.restart()
            scoreboard.left_point()
        if ball.xcor() < -bound:  # right point
            ball.restart()
            scoreboard.right_point()
        scoreboard.update_score()

    screen.exitonclick()


if __name__ == '__main__':
    main()