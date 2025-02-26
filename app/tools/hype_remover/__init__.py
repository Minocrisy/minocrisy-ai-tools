"""
Minocrisy AI Tools - Hype Remover Tool
Remove exaggerated claims and marketing hype from text.
"""
from flask import Blueprint

# Create a Blueprint for the Hype Remover tool
hype_remover_bp = Blueprint("hype_remover", __name__)

# Import routes to register them with the blueprint
from app.tools.hype_remover import routes
