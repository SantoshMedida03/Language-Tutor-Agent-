import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from sqlalchemy.orm import Session
from models.quiz import Quiz
from utils.auth import get_db
from schemas.chat import ChatState

class VocabularyQuizNode:
    """A node that generates a vocabulary quiz."""
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
        self.prompt_template = PromptTemplate.from_template(
            """
            You are an English vocabulary expert. Generate a 5-question multiple-choice quiz
            on a random set of common English vocabulary words. The questions should test the definition or usage of the words.

            Return the quiz as a single, valid JSON object. Do NOT include any other text, explanations, or markdown formatting.
            The JSON object must have a "questions" key, which is a list of 5 question objects.
            Each question object must have: "question_text", "choices" (a list of 4 strings), and "correct_answer".
            """
        )
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def __call__(self, state: ChatState) -> ChatState:
        quiz_str = self.chain.invoke({})
        
        if "```json" in quiz_str:
            quiz_str = quiz_str.split("```json")[1].strip()
        if "```" in quiz_str:
            quiz_str = quiz_str.split("```")[0].strip()

        try:
            quiz_data = json.loads(quiz_str)
            state.quiz = quiz_data
            
            db: Session = next(get_db())
            user_id = state.user_id
            
            questions_for_db = []
            answers_for_db = []
            if "questions" in quiz_data and isinstance(quiz_data["questions"], list):
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
                title="Vocabulary Quiz",
                questions=json.dumps(questions_for_db),
                answers=json.dumps(answers_for_db),
                owner_id=user_id,
                score=0.0
            )
            db.add(db_quiz)
            db.commit()
            
            state.tutor_response = "I've just created a new vocabulary quiz for you! You can find it in the Quiz section of your dashboard."
            
        except (json.JSONDecodeError, TypeError):
            state.quiz = {}
            state.tutor_response = "I had a little trouble creating a vocabulary quiz. Let's try again!"
            
        return state
