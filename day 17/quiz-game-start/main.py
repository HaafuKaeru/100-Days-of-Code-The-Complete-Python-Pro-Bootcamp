from question_model import Question
from data import question_data
from quiz_brain import QuizBrain


def main():
    # create list of Question objects with data from question_data
    question_bank = []
    for data in question_data:
        question_bank.append(Question(data['text'], data['answer']))

    # create quizbrain object
    quiz = QuizBrain(question_bank)

    while quiz.still_has_questions():
        quiz.next_question()

    print("You've completed the quiz.")
    print(f"Your final score was: {quiz.score}/{len(quiz.question_list)}")


if __name__ == '__main__':
    main()