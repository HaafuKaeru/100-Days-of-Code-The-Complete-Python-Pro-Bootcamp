from turtle import Turtle


class ScoreBoard(Turtle):

    def __init__(self):
        super().__init__()
        self.color('white')
        self.penup()
        self.hideturtle()
        self.left_score = 0
        self.right_score = 0
        self.update_score()

    def update_score(self):
        score_xcor = 100
        score_ycor = 190
        font = ('Courier', 60, 'normal')
        self.clear()
        self.goto(-score_xcor, score_ycor)
        self.write(self.left_score, align='center', font=font)
        self.goto(score_xcor, score_ycor)
        self.write(self.right_score, align='center', font=font)

    def left_point(self):
        self.left_score += 1

    def right_point(self):
        self.right_score += 1
