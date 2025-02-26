"""
Minocrisy AI Tools - Main Routes
Contains the main routes for the application.
"""
from flask import Blueprint, render_template, jsonify, current_app

# Create a Blueprint for the main routes
main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    """Render the main page of the application."""
    return render_template("index.html")

@main_bp.route("/api/tools")
def list_tools():
    """Return a list of available tools."""
    tools = [
        {
            "id": "talking-head",
            "name": "Talking Head",
            "description": "Generate animated talking head videos from text input using ElevenLabs and RunwayML.",
            "endpoint": "/tools/talking-head"
        },
        {
            "id": "hype-remover",
            "name": "Hype Remover",
            "description": "Remove exaggerated claims and marketing hype from text.",
            "endpoint": "/tools/hype-remover"
        },
        {
            "id": "xai-chat",
            "name": "Grok Chat",
            "description": "Chat with xAI's Grok model for intelligent conversations and assistance.",
            "endpoint": "/tools/xai-chat",
            "api": "xai"
        },
        {
            "id": "hedra-character",
            "name": "Hedra Character Video",
            "description": "Generate character videos with synchronized speech using Hedra's API.",
            "endpoint": "/tools/hedra-character",
            "api": "hedra"
        }
    ]
    
    # Filter out tools that require APIs that aren't configured
    configured_apis = {
        "xai": bool(current_app.config.get("XAI_API_KEY")),
        "hedra": bool(current_app.config.get("HEDRA_API_KEY"))
    }
    
    filtered_tools = [
        tool for tool in tools 
        if not tool.get("api") or configured_apis.get(tool.get("api"), False)
    ]
    
    return jsonify(filtered_tools)

@main_bp.route("/api/status")
def api_status():
    """Return the status of the API integrations."""
    status = {
        "elevenlabs": bool(current_app.config.get("ELEVENLABS_API_KEY")),
        "openai": bool(current_app.config.get("OPENAI_API_KEY")),
        "runwayml": bool(current_app.config.get("RUNWAYML_API_KEY")),
        "xai": bool(current_app.config.get("XAI_API_KEY")),
        "hedra": bool(current_app.config.get("HEDRA_API_KEY"))
    }
    return jsonify(status)
