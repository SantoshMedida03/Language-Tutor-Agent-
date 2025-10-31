from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from utils import auth
from models.user import User
from models.story import Story
from models.quiz import Quiz
from utils.story_generator import generate_story_content
from utils.quiz_generator import generate_quiz_data
import json

router = APIRouter()

@router.get("/session/today")
async def get_or_create_today_session(db: Session = Depends(auth.get_db), current_user: User = Depends(auth.get_current_user)):
    """
    This is the definitive endpoint for starting a user's session.
    It gets or creates a story and its corresponding quiz for the current day.
    """
    # 1. Check for a story created today
    today_story = db.query(Story).filter(
        Story.owner_id == current_user.id,
        func.date(Story.created_at) == date.today()
    ).order_by(Story.id.desc()).first()

    # 2. If no story exists for today, create one
    if not today_story:
        try:
            story_text = generate_story_content()
            if not story_text or len(story_text) < 20:
                raise Exception("Generated story content was invalid.")
            
            today_story = Story(
                title="Today's Story",
                content=story_text,
                owner_id=current_user.id
            )
            db.add(today_story)
            db.commit()
            db.refresh(today_story)
        except Exception as e:
            print(f"Error generating story: {e}")
            raise HTTPException(status_code=500, detail="Could not generate today's story.")

    # 3. Check for a quiz for today's story
    today_quiz = db.query(Quiz).filter(
        Quiz.owner_id == current_user.id,
        func.date(Quiz.created_at) == date.today(),
        Quiz.title == "Today's Story Quiz"
    ).order_by(Quiz.id.desc()).first()

    # 4. If no quiz exists for today's story, create one
    if not today_quiz:
        quiz_data = generate_quiz_data(today_story.content)
        if not quiz_data or not quiz_data.get("questions"):
            # If quiz generation fails, we can proceed without it.
            return {"story": today_story, "quiz": None}

        questions_for_db = []
        answers_for_db = []
        for q in quiz_data["questions"]:
            questions_for_db.append(f"{q.get('question_text', '')}\n" + "\n".join([f"{chr(65+i)}) {c}" for i, c in enumerate(q.get('choices', []))]))
            if q.get('correct_answer') in q.get('choices', []):
                answers_for_db.append(chr(65 + q.get('choices').index(q.get('correct_answer'))))

        today_quiz = Quiz(
            title="Today's Story Quiz",
            questions=json.dumps(questions_for_db),
            answers=json.dumps(answers_for_db),
            owner_id=current_user.id,
            score=0.0
        )
        db.add(today_quiz)
        db.commit()
        db.refresh(today_quiz)

    return {"story": today_story, "quiz": today_quiz}
