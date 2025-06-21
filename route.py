from flask import Blueprint, request, jsonify
from chatbot import generate_response, chat_history_ids
import torch

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    chat_history_list = request.json.get("chat_history_ids", None)

    chat_history_ids = torch.tensor(chat_history_list, dtype=torch.long) if chat_history_list else None
    response, updated_history = generate_response(user_input, chat_history_ids)
    updated_history_list = updated_history.tolist() if updated_history is not None else None

    return jsonify({
        "response": response,
        "chat_history_ids": updated_history_list
    })
