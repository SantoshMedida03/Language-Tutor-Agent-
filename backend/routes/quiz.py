from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import quiz as quiz_schema
from utils import auth
from models.quiz import Quiz
from models.user import User

router = APIRouter()

@router.post("/quiz", response_model=quiz_schema.Quiz)
async def generate_quiz(db: Session = Depends(auth.get_db), current_user: User = Depends(auth.get_current_user)):
    quiz = db.query(Quiz).filter(Quiz.owner_id == current_user.id).order_by(Quiz.id.desc()).first()
    if not quiz:
        return quiz_schema.Quiz(id=0, owner_id=current_user.id, title="No Quiz Yet", questions="[]", answers="[]", score=0.0)
    return quiz
