"""Routes for the backend."""

import json
import os

from fastapi import Response
import src.db.database as database
from jaclang import jac_import

agent_mod = jac_import("agent", os.path.dirname(__file__))
assert hasattr(agent_mod, "get_answer"), "Error importing get_answer from agent module"
assert hasattr(agent_mod, "summarize_chat_history"), "Error importing chat_history_summarizer from agent module"

def answer_question(chat_id: str, body: dict) -> Response:
    """Answer a question for a chat."""
    try:
        question = body.get("question")
        if not question:
            raise ValueError("Question not provided")
        chat_history = database.get_chat(chat_id)
        chat_summary = agent_mod.summarize_chat_history(chat_history)
        answer = agent_mod.get_answer(question, chat_summary)
        return Response(content=json.dumps(answer.to_dict()), status_code=200, media_type="application/json")
    except Exception as e:
        return Response(content=json.dumps({"error": str(e)}), status_code=400, media_type="application/json")

def get_chats() -> Response:
    """Get all chats."""
    try:
        return Response(content=json.dumps(database.get_chats()), status_code=200, media_type="application/json")
    except Exception as e:
        return Response(content=json.dumps({"error": str(e)}), status_code=400, media_type="application/json")
    
def get_chat(chat_id: str) -> Response:
    """Get a chat by id."""
    try:
        return Response(content=json.dumps(database.get_chat(chat_id)), status_code=200, media_type="application/json")
    except Exception as e:
        return Response(content=json.dumps({"error": str(e)}), status_code=400, media_type="application/json")
    
def create_chat(body: dict) -> Response:
    """Create a chat."""
    try:
        chat_id = database.create_chat(body)
        return Response(content=json.dumps({"chat_id": chat_id}), status_code=200, media_type="application/json")
    except Exception as e:
        return Response(content=json.dumps({"error": str(e)}), status_code=400, media_type="application/json")
    
def delete_chat(chat_id: str) -> Response:
    """Delete a chat by id."""
    try:
        database.delete_chat(chat_id)
        return Response(content=json.dumps({"chat_id": chat_id}), status_code=200, media_type="application/json")
    except Exception as e:
        return Response(content=json.dumps({"error": str(e)}), status_code=400, media_type="application/json")