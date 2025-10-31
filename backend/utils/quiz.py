import json

def calculate_score(user_answers: dict, correct_answers_json: str) -> float:
    """
    Calculates the user's score based on their submitted answers.

    Args:
        user_answers: A dictionary where keys are question indices (as strings)
                      and values are the user's selected choice (e.g., "A) The house").
        correct_answers_json: A JSON string containing a list of the correct answer letters (e.g., '["A", "C", "B"]').

    Returns:
        The percentage of correct answers as a float.
    """
    try:
        correct_answers = json.loads(correct_answers_json)
        if not isinstance(correct_answers, list):
            return 0.0

        correct_count = 0
        total_questions = len(correct_answers)

        for i, correct_letter in enumerate(correct_answers):
            user_answer_full = user_answers.get(str(i))
            if user_answer_full:
                # The user's answer is the full text, e.g., "A) The house". We just need the first letter.
                user_letter = user_answer_full.split(')')[0].strip()
                if user_letter == correct_letter:
                    correct_count += 1
        
        return (correct_count / total_questions) * 100 if total_questions > 0 else 0.0

    except (json.JSONDecodeError, TypeError, AttributeError):
        return 0.0
