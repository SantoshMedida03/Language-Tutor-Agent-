from sqlalchemy.orm import Session
from ...models.user import User
from ...utils.auth import get_db

from ...schemas.chat import ChatState

class AdaptationNode:
    def __call__(self, state: ChatState) -> ChatState:
        quiz_accuracy = state.quiz_accuracy or 0
        
        db: Session = next(get_db())
        user_id = state.user_id
        user = db.query(User).filter(User.id == user_id).first()
        
        if user:
            if quiz_accuracy > 0.85:
                user.learning_level += 0.1
            elif quiz_accuracy < 0.6:
                user.learning_level -= 0.1
            
            db.commit()
            
        return state