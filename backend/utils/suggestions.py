def get_suggestion(score: float) -> str:
    """
    Generates a personalized suggestion based on the user's quiz score.
    """
    if score == 100:
        return "Perfect score! You have an excellent understanding of the material. Keep up the fantastic work!"
    elif score >= 80:
        return "Great job! You have a strong grasp of the concepts. Review the questions you missed to solidify your knowledge."
    elif score >= 60:
        return "Good effort! You're on the right track. Re-reading the story and focusing on the vocabulary might be helpful."
    elif score >= 40:
        return "You're making progress! Don't be discouraged. Let's try reviewing the story and vocabulary together."
    else:
        return "That was a good first attempt! Repetition is key. Let's read the story again and then try another quiz."
