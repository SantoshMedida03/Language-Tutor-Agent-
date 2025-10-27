from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from sqlalchemy.orm import Session
from models.story import Story
from utils.auth import get_db

from schemas.chat import ChatState

from models.user import User

class StoryGenerationNode:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
        self.prompt_template = PromptTemplate.from_template(
            "Generate a short story for a language learner. The story should be about {topic} "
            "and should incorporate the following vocabulary words: {vocabulary}. "
            "The story should be at a {difficulty} level."
        )
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def __call__(self, state: ChatState) -> ChatState:
        db: Session = next(get_db())
        user = db.query(User).filter(User.id == state.user_id).first()

        topic = user.interests if user and user.interests else "a friendly robot"
        difficulty_map = {1: "beginner", 2: "intermediate", 3: "advanced"}
        difficulty = difficulty_map.get(int(user.learning_level), "beginner") if user else "beginner"
        
        vocabulary = state.new_vocabulary or "learning, robot, friend"
        story_content = self.chain.invoke({"topic": topic, "vocabulary": str(vocabulary), "difficulty": difficulty})
        state.story = story_content
        
        user_id = state.user_id
        db_story = Story(
            title=f"A story about {topic}",
            content=story_content,
            owner_id=user_id,
        )
        db.add(db_story)
        db.commit()
        
        return state