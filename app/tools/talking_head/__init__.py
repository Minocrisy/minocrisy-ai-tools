"""
Minocrisy AI Tools - Talking Head Tool
Generate animated talking head videos from text input using ElevenLabs and RunwayML.
"""
from flask import Blueprint

# Create a Blueprint for the Talking Head tool
talking_head_bp = Blueprint("talking_head", __name__)

# Import routes to register them with the blueprint
from app.tools.talking_head import routes
