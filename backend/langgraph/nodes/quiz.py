from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import json
from sqlalchemy.orm import Session
from ...models.quiz import Quiz
from ...utils.auth import get_db

from ...schemas.chat import ChatState

class QuizNode:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
        self.prompt_template = PromptTemplate.from_template(
            "Generate a quiz with multiple-choice and fill-in-the-blank questions based on the following story: {story}. "
            "The quiz should test the reader's comprehension of the story and their understanding of the vocabulary words: {vocabulary}. "
            "Return the quiz in a JSON format with 'questions' and 'answers' keys."
        )
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def __call__(self, state: ChatState) -> ChatState:
        story = state.story
        vocabulary = state.new_vocabulary or ""
        quiz_str = self.chain.invoke({"story": story, "vocabulary": str(vocabulary)})
        
        try:
            quiz_data = json.loads(quiz_str)
            state.quiz = quiz_data
            
            db: Session = next(get_db())
            user_id = state.user_id
            db_quiz = Quiz(
                title="Story Quiz",
                questions=json.dumps(quiz_data.get("questions")),
                answers=json.dumps(quiz_data.get("answers")),
                owner_id=user_id,
                score=0.0
            )
            db.add(db_quiz)
            db.commit()
        except json.JSONDecodeError:
            state.quiz = {}
            
        return state