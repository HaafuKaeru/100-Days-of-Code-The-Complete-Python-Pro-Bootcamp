from question_model import Question
from data import get_data
from quiz_brain import QuizBrain
from ui import QuizInterface


def main():
    topic = "history"
    question_bank = []
    for question in get_data(topic):
        question_text = question["question"]
        question_answer = question["correct_answer"]
        new_question = Question(question_text, question_answer)
        question_bank.append(new_question)

    quiz = QuizBrain(question_bank)
    quiz_ui = QuizInterface(quiz, topic)

    print(quiz_ui.quiz.score)

    print("")
    print()


if __name__ == '__main__':
    main()