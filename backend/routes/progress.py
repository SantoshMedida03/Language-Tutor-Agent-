from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import progress_log as progress_schema
from utils import auth
from models.progress_log import ProgressLog
from models.user import User
from typing import List

router = APIRouter()

@router.get("/progress", response_model=List[progress_schema.ProgressLog])
async def get_progress(db: Session = Depends(auth.get_db), current_user: User = Depends(auth.get_current_user)):
    progress = db.query(ProgressLog).filter(ProgressLog.owner_id == current_user.id).all()
    return progress
