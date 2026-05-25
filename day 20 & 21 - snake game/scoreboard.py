from turtle import Turtle


ALIGNMENT = 'center'
FONT = ('Consolas', 16, 'normal')

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.color('white')
        self.score = 0
        self.penup()
        self.goto(0, 270)
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(
            f"Score: {self.score}",
            font=FONT,
            align=ALIGNMENT
        )

    def increase_score(self):
        self.score += 1
        self.update_score()

    def game_over(self):
        self.goto(0, 0)
        self.write("Game Over!", font=FONT, align=ALIGNMENT)