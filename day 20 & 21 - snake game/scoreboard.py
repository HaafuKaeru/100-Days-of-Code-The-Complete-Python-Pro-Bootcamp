from turtle import Turtle


ALIGNMENT = 'center'
FONT = ('Consolas', 16, 'normal')

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.color('white')
        self.score = 0
        self.high_score = 0
        self.load_high_score()
        self.penup()
        self.goto(0, 270)
        self.update_score()

    def update_score(self):
        self.clear()
        self.load_high_score()
        self.write(
            f"Score: {self.score} High Score: {self.high_score}",
            font=FONT,
            align=ALIGNMENT
        )

    def increase_score(self):
        self.score += 1
        self.update_score()

    def load_high_score(self):
        with open("data.txt", 'r') as f:
            self.high_score = int(f.read())

    @staticmethod
    def update_high_score(self, new_score):
        with open("data.txt", 'w') as f:
            f.write(str(new_score))

    def reset_game(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.update_high_score(self.score)
        self.score = 0
        self.update_score()
