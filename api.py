import os

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from langchain_groq import ChatGroq
from pydantic import BaseModel

from backend.audio_utils import trim_trailing_silence

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Configure CORS to allow requests from your Flutter app
# This is crucial for Flutter Web to communicate with localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Groq model
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("Warning: GROQ_API_KEY not found. Please check your .env file.")

chat = ChatGroq(temperature=0.6, model="llama-3.3-70b-versatile", api_key=api_key)
client = Groq(api_key=api_key)

# In-memory storage for conversation history
conversations = {}


# Define the request body structure
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


def process_conversation(session_id: str, user_message: str) -> str:
    """Helper function to handle conversation history and LLM invocation."""
    # Initialize history if new session
    if session_id not in conversations:
        conversations[session_id] = [
            (
                "system",
                "You are a friendly English tutor. Your goal is to help the user practice English conversation. Speak only in English. If the user makes a grammatical error, gently correct them inside your response.",
            )
        ]

    # Add user message to history
    conversations[session_id].append(("human", user_message))

    # Limit history to last 10 messages to save tokens (keeping system prompt)
    if len(conversations[session_id]) > 11:
        conversations[session_id] = [conversations[session_id][0]] + conversations[session_id][-10:]

    # Get response from Groq
    response = chat.invoke(conversations[session_id])

    # Add AI response to history
    conversations[session_id].append(("ai", response.content))

    return response.content


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response_content = process_conversation(request.session_id, request.message)
        return {"response": response_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/audio")
async def chat_audio_endpoint(file: UploadFile = File(...), session_id: str = Form("default")):
    try:
        # 1. Read and trim audio
        audio_bytes = await file.read()
        trimmed_audio = trim_trailing_silence(audio_bytes)

        # 2. Transcribe using Whisper (Groq)
        transcription = client.audio.transcriptions.create(
            file=(file.filename, trimmed_audio), model="whisper-large-v3", language="en"
        )
        user_message = transcription.text

        # 3. Process conversation logic
        response_content = process_conversation(session_id, user_message)

        return {"response": response_content, "transcription": user_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
