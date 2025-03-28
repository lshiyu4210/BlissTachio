from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.api.database import get_db  # Import from database.py
from backend.api.model import User
from pydantic import BaseModel, EmailStr
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# FastAPI app
app = FastAPI()

# Pydantic Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# User Registration
@app.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Correct way to query users table
    result = await db.execute(select(User).filter(User.email == user.email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password and store user
    hashed_password = generate_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "User registered successfully"}

# User Login
@app.post("/login")
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user.email))
    db_user = result.scalars().first()

    if not db_user or not check_password_hash(db_user.password_hash, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"user_id": db_user.id, "email": db_user.email}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
