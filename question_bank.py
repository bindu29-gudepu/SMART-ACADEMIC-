# question_bank.py

def generate_questions_from_syllabus(lesson):

    easy_questions = []
    medium_questions = []
    hard_questions = []

    # ---------- EASY LEVEL (Basic Understanding) ----------
    for i in range(1, 9):
        easy_questions.append({
            "question": f"{lesson}: Basic Concept Question {i}",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Option A"
        })

    # ---------- MEDIUM LEVEL (Application) ----------
    for i in range(1, 9):
        medium_questions.append({
            "question": f"{lesson}: Understanding Level Question {i}",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Option A"
        })

    # ---------- HARD LEVEL (Analytical) ----------
    for i in range(1, 9):
        hard_questions.append({
            "question": f"{lesson}: Analytical Level Question {i}",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Option A"
        })

    return {
        "Easy": easy_questions,
        "Medium": medium_questions,
        "Hard": hard_questions
    }
