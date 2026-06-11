import tkinter as tk
from quiz_brain import QuizBrain

# set higher resolution tkinter rendering
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(True)


THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = tk.Tk()
        self.window.title("Quizzler")
        self.window.configure(bg=THEME_COLOR, padx=20, pady=20)

        # score label
        self.score_label = tk.Label()
        self.score_label.configure(
            text="Score: 0",
            font=("Arial", 10, "bold"),
            foreground="white",
            background=THEME_COLOR,
            padx=20, pady=20,
        )
        self.score_label.grid(row=0, column=1)

        # main canvas with question
        self.canvas_width = 300
        self.canvas_height = 250
        self.canvas = tk.Canvas(
            width=self.canvas_width,
            height=self.canvas_height,
            background="white",
            highlightthickness=0,
        )
        self.question_text = self.canvas.create_text(
            self.canvas_width / 2,
            self.canvas_height / 2,
            width=290,
            text="Sample Text",
            font=("Arial", 15, "italic"),
            fill=THEME_COLOR
        )
        self.canvas.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

        # buttons
        true_img = tk.PhotoImage(file="images/true.png")
        false_img = tk.PhotoImage(file="images/false.png")
        self.true_button = tk.Button()
        self.true_button.configure(image=true_img, borderwidth=0, command=self.true_pressed)
        self.true_button.grid(row=2, column=0, padx=20, pady=20)
        self.false_button = tk.Button()
        self.false_button.configure(image=false_img, borderwidth=0, command=self.false_pressed)
        self.false_button.grid(row=2, column=1, padx=20, pady=20)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.update_canvas()
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text=f"You've completed the quiz\n\nYour final score was: {self.quiz.score}/{self.quiz.question_number}")

    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right: bool):
        self.canvas.configure(background="green" if is_right else "red")
        self.window.after(1000, func=self.get_next_question)

    def update_canvas(self):
        self.canvas.configure(background="white")
        self.score_label.configure(text=f"Score: {self.quiz.score}")