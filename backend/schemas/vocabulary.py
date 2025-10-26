from pydantic import BaseModel
from datetime import date

class VocabularyBase(BaseModel):
    word: str
    meaning: str
    example: str
    status: str
    last_review_date: date
    next_review_date: date

class VocabularyCreate(VocabularyBase):
    pass

class Vocabulary(VocabularyBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
