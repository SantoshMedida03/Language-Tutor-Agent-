from pydantic import BaseModel
from typing import List, Dict, Any

class ChatMessage(BaseModel):
    text: str

class ChatState(BaseModel):
    user_id: int
    user_message: str
    tutor_response: str
    new_vocabulary: List[Dict[str, Any]]
    story: str
    quiz: Dict[str, Any]
    quiz_accuracy: float

