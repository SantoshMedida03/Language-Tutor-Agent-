from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from schemas import story as story_schema
from utils import auth
from models.story import Story
from models.user import User
from utils.story_generator import generate_story_content

router = APIRouter()

@router.get("/story", response_model=story_schema.Story)
async def get_todays_story(db: Session = Depends(auth.get_db), current_user: User = Depends(auth.get_current_user)):
    """
    Gets the story for the current day. If one does not exist, it generates,
    saves, and returns a new one. Includes robust error handling.
    """
    today_story = db.query(Story).filter(
        Story.owner_id == current_user.id,
        func.date(Story.created_at) == date.today()
    ).order_by(Story.id.desc()).first()

    if today_story:
        return today_story

    try:
        story_text = generate_story_content()
        if not story_text or len(story_text) < 20:
            raise Exception("Generated story content was invalid.")

        new_story = Story(
            title="Today's Story",
            content=story_text,
            owner_id=current_user.id
        )
        db.add(new_story)
        db.commit()
        db.refresh(new_story)
        return new_story
    except Exception as e:
        print(f"Error generating story: {e}")
        # Return a story object with an error message that the frontend can display
        return story_schema.Story(
            id=0,
            owner_id=current_user.id,
            title="Could Not Generate Story",
            content="There was an error generating today's story. This might be due to a network issue. Please try refreshing the page."
        )
