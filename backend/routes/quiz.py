from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from schemas import quiz as quiz_schema
from utils import auth
from models.quiz import Quiz
from models.story import Story
from models.user import User
from typing import Dict
from utils.quiz import calculate_score
from utils.suggestions import get_suggestion
from utils.quiz_generator import generate_quiz_data
import json

router = APIRouter()

@router.get("/quiz", response_model=quiz_schema.Quiz)
async def get_latest_quiz(db: Session = Depends(auth.get_db), current_user: User = Depends(auth.get_current_user)):
    """
    Fetches the most recent quiz for the user, regardless of its title or type.
    This is the single source of truth for the dashboard's quiz component.
    """
    latest_quiz = db.query(Quiz).filter(Quiz.owner_id == current_user.id).order_by(Quiz.id.desc()).first()

    if not latest_quiz:
        return quiz_schema.Quiz(id=0, owner_id=current_user.id, title="No Quiz Available", questions="[]", answers="[]", score=0.0)

    return latest_quiz

@router.post("/quiz/submit")
async def submit_quiz(
    answers: Dict[str, str], 
    db: Session = Depends(auth.get_db), 
    current_user: User = Depends(auth.get_current_user)
):
    db_quiz = db.query(Quiz).filter(Quiz.owner_id == current_user.id).order_by(Quiz.id.desc()).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="No quiz found to submit.")

    score = calculate_score(answers, db_quiz.answers)
    suggestion = get_suggestion(score)
    db_quiz.score = score
    db.commit()

    return {"score": score, "suggestion": suggestion}
