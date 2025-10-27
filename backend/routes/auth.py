from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas import user as user_schema, token as token_schema
from models import user as user_model
from utils import auth

router = APIRouter()

@router.post("/signup", response_model=user_schema.User)
def signup(user: user_schema.UserCreate, db: Session = Depends(auth.get_db)):
    db_user = db.query(models.user.User).filter(models.user.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.user.User(
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

@router.post("/login", response_model=token_schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    user = db.query(models.user.User).filter(models.user.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}