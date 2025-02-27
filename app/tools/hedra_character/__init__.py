"""
Minocrisy AI Tools - Hedra Character Video Tool
Generate character videos with synchronized speech using Hedra's API.
"""
from flask import Blueprint

# Create a Blueprint for the Hedra Character Video tool
hedra_character_bp = Blueprint("hedra_character", __name__)

# Import routes to register them with the blueprint
from app.tools.hedra_character import routes
