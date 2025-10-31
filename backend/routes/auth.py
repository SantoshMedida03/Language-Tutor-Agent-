from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from schemas import user as user_schema, token as token_schema
from utils import auth
from utils.auth import get_db
from models import user as user_model

router = APIRouter()

@router.post("/signup", response_model=user_schema.User)
def signup(user: user_schema.UserCreate, db: Session = Depends(auth.get_db)):
    db_user = db.query(user_model.User).filter(user_model.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = user_model.User(
        username=user.username,
        hashed_password=hashed_password,
        preferred_language=user.preferred_language,
        learning_level=user.learning_level,
        interests=user.interests,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

from models.story import Story
from models.quiz import Quiz

@router.post("/token", response_model=token_schema.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Clear previous session data to ensure a fresh start
    db.query(Story).filter(Story.owner_id == user.id).delete()
    db.query(Quiz).filter(Quiz.owner_id == user.id).delete()
    db.commit()

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}