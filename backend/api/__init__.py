"""BlissTachio REST API"""
from fastapi import FastAPI
from backend.api.main import home, chat
from backend.api.register import register_user, login_user

app = FastAPI()

# Include routes
app.add_api_route("/", home, methods=["GET"])
app.add_api_route("/chat", chat, methods=["POST"])
app.add_api_route("/register", register_user, methods=["POST"])
app.add_api_route("/login", login_user, methods=["POST"])