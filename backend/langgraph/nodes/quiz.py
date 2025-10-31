from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import json
from sqlalchemy.orm import Session
from models.quiz import Quiz
from utils.auth import get_db

from schemas.chat import ChatState

from models.story import Story
from models.quiz import Quiz
from sqlalchemy.orm import Session
from utils.auth import get_db
from schemas.chat import ChatState
from utils.quiz_generator import generate_quiz_data
import json

class QuizNode:
    def __call__(self, state: ChatState) -> ChatState:
        db: Session = next(get_db())
        user_id = state.user_id

        latest_story = db.query(Story).filter(Story.owner_id == user_id).order_by(Story.id.desc()).first()

        if not latest_story:
            state.tutor_response = "Happy to create a quiz for you! But first, I need a story to base it on. Please ask me to 'generate a story' and then we can do a quiz on it."
            return state

        quiz_data = generate_quiz_data(latest_story.content)
        
        if not quiz_data.get("questions"):
            state.quiz = {}
            state.tutor_response = "I had a little trouble creating a quiz for that story. Let's try another one!"
            return state

        state.quiz = quiz_data
        
        questions_for_db = []
        answers_for_db = []
        for q in quiz_data["questions"]:
            question_text = q.get("question_text", "")
            choices = q.get("choices", [])
            formatted_choices = [f"{chr(65+i)}) {choice}" for i, choice in enumerate(choices)]
            questions_for_db.append(f"{question_text}\n" + "\n".join(formatted_choices))
            correct_answer_text = q.get("correct_answer")
            if correct_answer_text in choices:
                correct_index = choices.index(correct_answer_text)
                answers_for_db.append(chr(65 + correct_index))

        db_quiz = Quiz(
            title="Story Quiz",
            questions=json.dumps(questions_for_db),
            answers=json.dumps(answers_for_db),
            owner_id=user_id,
            score=0.0
        )
        db.add(db_quiz)
        db.commit()
        
        state.tutor_response = "I've just created a quiz for you based on that story! You can find it in the Quiz section of your dashboard."
            
        return state