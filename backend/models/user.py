from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from ..config.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    preferred_language = Column(String)
    learning_level = Column(Float)
    interests = Column(String)

    vocabularies = relationship("Vocabulary", back_populates="owner")
    stories = relationship("Story", back_populates="owner")
    quizzes = relationship("Quiz", back_populates="owner")
    progress_logs = relationship("ProgressLog", back_populates="owner")