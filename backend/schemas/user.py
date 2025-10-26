from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    preferred_language: str
    learning_level: float
    interests: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True