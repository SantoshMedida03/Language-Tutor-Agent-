from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv
from config.database import engine, Base
from routes import auth, chat, story, quiz, vocab, progress
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(story.router)
app.include_router(quiz.router)
app.include_router(vocab.router)
app.include_router(progress.router)