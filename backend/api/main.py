from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from dotenv import load_dotenv
import openai
import os

from backend.api.model import Message
from backend.api.database import get_db

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

# Initialize FastAPI app
app = FastAPI()

# Redirect root to login page
@app.get("/")
def home():
    return RedirectResponse(url="/frontend/login.html")

# Request model for /chat endpoint
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(chat_request: ChatRequest, request: Request, db: AsyncSession = Depends(get_db)):
    # Extract user_id from token (same as before)
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    # Store the user message without response first
    message = Message(user_id=user_id, content=chat_request.message)
    db.add(message)
    await db.commit()
    await db.refresh(message)

    # Get OpenAI response
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": chat_request.message}]
        )
        reply = response.choices[0].message.content

        # Update the message with assistant's reply
        message.response = reply
        await db.commit()

        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")

