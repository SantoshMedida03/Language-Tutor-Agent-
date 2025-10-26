from pydantic import BaseModel

class QuizBase(BaseModel):
    title: str
    questions: str
    answers: str
    score: float

class QuizCreate(QuizBase):
    pass

class Quiz(QuizBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
