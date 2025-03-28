from fastapi import FastAPI, HTTPException
import openai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to BlissTachio!"}

@app.post("/chat")
async def chat(query: str):
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)  # New API client structure

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}]
        )

        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

