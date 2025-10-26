from pydantic import BaseModel
from datetime import date

class ProgressLogBase(BaseModel):
    date: date
    quiz_accuracy: float
    words_learned: int

class ProgressLogCreate(ProgressLogBase):
    pass

class ProgressLog(ProgressLogBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
