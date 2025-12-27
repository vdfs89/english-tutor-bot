import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Initialize the Groq model
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("Warning: GROQ_API_KEY not found. Please check your .env file.")

chat = ChatGroq(temperature=0.6, model="llama-3.3-70b-versatile", api_key=api_key)

# In-memory storage for conversation history
conversations = {}


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

    return str(response.content)
