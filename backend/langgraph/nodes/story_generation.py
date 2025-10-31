from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from sqlalchemy.orm import Session
from models.story import Story
from utils.auth import get_db

from schemas.chat import ChatState

from models.user import User

from models.story import Story
from sqlalchemy.orm import Session
from utils.auth import get_db
from schemas.chat import ChatState
from utils.story_generator import generate_story_content

class StoryGenerationNode:
    def __call__(self, state: ChatState) -> ChatState:
        story_text = generate_story_content()
        
        db: Session = next(get_db())
        user_id = state.user_id
        db_story = Story(
            title="Generated Story",
            content=story_text,
            owner_id=user_id
        )
        db.add(db_story)
        db.commit()

        state.story = story_text
        state.tutor_response = story_text
        return state