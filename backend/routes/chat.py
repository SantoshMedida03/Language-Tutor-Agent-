from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from schemas import chat as chat_schema
from utils import auth
from langgraph.graph_builder import create_graph
from schemas.chat import ChatState
from models.user import User

router = APIRouter()

@router.post("/chat")
async def chat(message: chat_schema.ChatMessage, db: Session = Depends(auth.get_db), current_user: User = Depends(auth.get_current_user)):
    graph = create_graph()
    initial_state = ChatState(
        user_id=current_user.id,
        user_message=message.text,
        tutor_response="",
        new_vocabulary=[],
        story="",
        quiz={},
        quiz_accuracy=0.0
    )
    
    # Run the blocking invoke call in a thread pool to avoid freezing the server
    final_state = await run_in_threadpool(graph.invoke, initial_state)
    
    return {"message": final_state.tutor_response}
