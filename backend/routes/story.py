from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import story as story_schema
from utils import auth
from models.story import Story
from models.user import User

router = APIRouter()

@router.get("/story", response_model=story_schema.Story)
async def get_story(db: Session = Depends(auth.get_db), current_user: User = Depends(auth.get_current_user)):
    story = db.query(Story).filter(Story.owner_id == current_user.id).order_by(Story.id.desc()).first()
    if not story:
        return story_schema.Story(id=0, owner_id=current_user.id, title="Welcome!", content="Start a conversation in the chat to generate your first story.")
    return story
