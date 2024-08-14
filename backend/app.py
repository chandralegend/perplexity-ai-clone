"""Backend Server for Perplexity AI Clone."""

from fastapi import FastAPI

from src.routes import answer_question, create_chat, delete_chat, get_chats, get_chat

app = FastAPI()

app.add_api_route("/api/v1/get_chats", get_chats, methods=["GET"])
app.add_api_route("/api/v1/get_chats/{chat_id}", get_chat, methods=["GET"])
app.add_api_route("/api/v1/create_chat", create_chat, methods=["POST"])
app.add_api_route("/api/v1/delete_chat/{chat_id}", delete_chat, methods=["DELETE"])
app.add_api_route("/api/v1/get_chats/{chat_id}/answer", answer_question, methods=["POST"])