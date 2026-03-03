# quiz_engine.py

from question_bank import generate_questions_from_syllabus

def get_auto_difficulty(previous_score):

    if previous_score >= 75:
        return "Hard"
    elif previous_score >= 40:
        return "Medium"
    else:
        return "Easy"


def generate_quiz(lesson, difficulty):

    all_questions = generate_questions_from_syllabus(lesson)

    return all_questions[difficulty]
