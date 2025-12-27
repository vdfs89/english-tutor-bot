import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from pydantic import BaseModel

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

# In-memory storage for conversation history
conversations = {}


# Define the request body structure
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        session_id = request.session_id

        # Initialize history if new session
        if session_id not in conversations:
            conversations[session_id] = [
                (
                    "system",
                    "You are a friendly English tutor. Your goal is to help the user practice English conversation. Speak only in English. If the user makes a grammatical error, gently correct them inside your response.",
                )
            ]

        # Add user message to history
        conversations[session_id].append(("human", request.message))

        # Limit history to last 10 messages to save tokens (keeping system prompt)
        if len(conversations[session_id]) > 11:
            conversations[session_id] = [conversations[session_id][0]] + conversations[session_id][
                -10:
            ]

        # Get response from Groq
        response = chat.invoke(conversations[session_id])

        # Add AI response to history
        conversations[session_id].append(("ai", response.content))

        return {"response": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
