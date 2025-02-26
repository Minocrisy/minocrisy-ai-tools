"""
Minocrisy AI Tools - xAI Chat Tool
Chat with xAI's Grok model for intelligent conversations and assistance.
"""
from flask import Blueprint

# Create a Blueprint for the xAI Chat tool
xai_chat_bp = Blueprint("xai_chat", __name__)

# Import routes to register them with the blueprint
from app.tools.xai_chat import routes
