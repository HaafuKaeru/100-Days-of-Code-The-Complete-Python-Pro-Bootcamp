import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard


FINISH_LINE_Y = 280


def main():

    screen = Screen()
    screen.setup(width=600, height=600)
    screen.tracer(0)

    player = Player()
    car_manager = CarManager()
    scoreboard = Scoreboard()

    screen.listen()
    screen.onkeypress(player.move_up, 'Up')

    game_is_on = True
    while game_is_on:
        time.sleep(0.1)
        car_manager.spawn_car()
        car_manager.move_cars()
        screen.update()

        # detect player collision with cars
        for car in car_manager.cars_in_middle:
            if player.distance(car.xcor(), car.ycor()) <= 20:
                scoreboard.game_over()
                game_is_on = False

        # player successfully crosses road
        if player.ycor() >= FINISH_LINE_Y:
            player.reposition()
            car_manager.restart_cars()
            scoreboard.level_up()

    screen.exitonclick()


if __name__ == '__main__':
    main()