"""BlissTachio REST API"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from backend.api.main import home, chat
from backend.api.register import register_user, login_user
from backend.api.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # create all tables before the app starts
    yield

app = FastAPI(lifespan=lifespan)

# Mount frontend static files
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

# Include routes
app.add_api_route("/", home, methods=["GET"])
app.add_api_route("/chat", chat, methods=["POST"])
app.add_api_route("/register", register_user, methods=["POST"])
app.add_api_route("/login", login_user, methods=["POST"])