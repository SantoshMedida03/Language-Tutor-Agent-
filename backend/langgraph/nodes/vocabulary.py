from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import json
from sqlalchemy.orm import Session
from models.vocabulary import Vocabulary
from utils.auth import get_db
from schemas.chat import ChatState
from datetime import date, timedelta

class VocabularyNode:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
        self.prompt_template = PromptTemplate.from_template(
            "Extract any new vocabulary words from this conversation: {conversation}. "
            "For each word, provide the word, its meaning, and an example sentence. "
            "Return the information in a JSON array format, with each object having 'word', 'meaning', and 'example' keys."
        )
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def __call__(self, state: ChatState) -> ChatState:
        conversation = f"User: {state.user_message}\nTutor: {state.tutor_response}"
        new_vocabulary_str = self.chain.invoke({"conversation": conversation})
        
        try:
            new_vocabulary = json.loads(new_vocabulary_str)
            state.new_vocabulary = new_vocabulary
            
            db: Session = next(get_db())
            user_id = state.user_id
            for vocab_item in new_vocabulary:
                db_vocab = Vocabulary(
                    word=vocab_item["word"],
                    meaning=vocab_item["meaning"],
                    example=vocab_item["example"],
                    status="new",
                    owner_id=user_id,
                    last_review_date=date.today(),
                    next_review_date=date.today() + timedelta(days=1),
                )
                db.add(db_vocab)
            db.commit()
        except json.JSONDecodeError:
            # Handle cases where the output is not valid JSON
            state.new_vocabulary = []

        return state
