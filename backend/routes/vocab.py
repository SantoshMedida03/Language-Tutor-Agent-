from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import vocabulary as vocab_schema
from utils import auth
from models.vocabulary import Vocabulary
from models.user import User
from typing import List

router = APIRouter()

@router.get("/vocab", response_model=List[vocab_schema.Vocabulary])
async def get_vocab(db: Session = Depends(auth.get_db), current_user: User = Depends(auth.get_current_user)):
    vocab = db.query(Vocabulary).filter(Vocabulary.owner_id == current_user.id).all()
    return vocab
