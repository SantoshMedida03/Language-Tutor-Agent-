from schemas.chat import ChatState
from models.story import Story
from sqlalchemy.orm import Session
from utils.auth import get_db
import re

class RouterNode:
    """
    A robust, deterministic router that correctly prioritizes conversation and
    validates state before routing to a feature.
    """
    def __call__(self, state: ChatState) -> dict:
        user_message = state.user_message.lower()
        db: Session = next(get_db())
        user_id = state.user_id

        # Define very specific keywords to avoid misinterpretation
        story_keywords = ['generate a story', 'tell me a story', 'create a story']
        comprehension_quiz_keywords = ['quiz on the story', 'comprehension quiz', 'test me on the story']
        grammar_pattern = r'\bgrammar\b'
        vocabulary_pattern = r'\bvocabulary\b'
        
        # Check for a grammar quiz request
        if re.search(grammar_pattern, user_message) and 'quiz' in user_message:
            return {"next_node": "grammar_quiz"}
            
        # Check for a vocabulary quiz request
        if re.search(vocabulary_pattern, user_message) and 'quiz' in user_message:
            return {"next_node": "vocabulary_quiz"}

        # Check for a story request
        if any(keyword in user_message for keyword in story_keywords):
            return {"next_node": "story"}

        # Check for a comprehension quiz request
        if any(keyword in user_message for keyword in comprehension_quiz_keywords):
            latest_story = db.query(Story).filter(Story.owner_id == user_id).order_by(Story.id.desc()).first()
            if latest_story:
                return {"next_node": "quiz"}
            else:
                state.tutor_response = "I'd be happy to give you a quiz, but we need a story first! Please ask me to 'generate a story'."
                return {"next_node": "end_conversation"}

        # Default to a normal conversation
        return {"next_node": "conversation"}