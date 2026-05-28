from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time


def main():
    screen = Screen()
    screen.setup(width=600, height=600)
    screen.bgcolor('black')
    screen.title("My Snake Game")
    screen.tracer(0)

    snake = Snake()
    food = Food()
    scoreboard = Scoreboard()

    screen.listen()
    screen.onkey(snake.up, 'Up')
    screen.onkey(snake.down, 'Down')
    screen.onkey(snake.left, 'Left')
    screen.onkey(snake.right, 'Right')

    game_is_on = True
    while game_is_on:
        screen.update()
        time.sleep(0.1)
        snake.move()

        # detect collision with food
        if snake.head.distance(food) < 15:
            food.refresh()
            snake.extend()
            scoreboard.increase_score()

        # detect collision with wall
        wall_distance = 280
        if (snake.head.xcor() < -wall_distance or
            snake.head.xcor() > wall_distance or
            snake.head.ycor() < -wall_distance or
            snake.head.ycor() > wall_distance
        ):
            scoreboard.reset_game()
            snake.reset_snake()
            food.refresh()

        # detect collision with tail
        for segment in snake.segments[1:]:
            if snake.head.distance(segment) < 10:
                scoreboard.reset_game()
                snake.reset_snake()
                food.refresh()

    screen.exitonclick()


if __name__ == '__main__':
    main()