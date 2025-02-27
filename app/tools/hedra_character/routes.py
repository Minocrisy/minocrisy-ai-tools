"""
Minocrisy AI Tools - Hedra Character Video Routes
Routes for the Hedra Character Video tool.
"""
import os
from flask import request, jsonify, render_template, current_app, send_file, url_for
from werkzeug.utils import secure_filename
from app.tools.hedra_character import hedra_character_bp
from app.utils.hedra_api import generate_character_video, list_characters, list_voices
from app.utils.secrets import get_hedra_api_key

@hedra_character_bp.route("/", methods=["GET"])
def index():
    """Render the Hedra Character Video tool page."""
    return render_template("hedra_character/index.html")

@hedra_character_bp.route("/generate", methods=["POST"])
def generate():
    """
    Generate a character video using the Hedra API.
    
    Request JSON:
    {
        "text": "Text for the character to speak",
        "character_id": "Optional character ID",
        "voice_id": "Optional voice ID"
    }
    
    Returns:
    {
        "video_url": "URL to the generated video",
        "text": "Original text input"
    }
    """
    # Get Hedra API key
    hedra_api_key = get_hedra_api_key()
    
    # Check if API key is available
    if not hedra_api_key:
        return jsonify({"error": "Hedra API key not configured"}), 500
    
    # Get request data
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text input is required"}), 400
    
    text = data["text"]
    character_id = data.get("character_id")
    voice_id = data.get("voice_id")
    
    try:
        # Create a directory for storing videos if it doesn't exist
        videos_dir = os.path.join(current_app.static_folder, "videos")
        os.makedirs(videos_dir, exist_ok=True)
        
        # Generate a unique filename
        filename = secure_filename(f"hedra_{text[:20]}_{character_id or 'default'}_{voice_id or 'default'}.mp4")
        output_path = os.path.join(videos_dir, filename)
        
        # Generate the video using Hedra API
        video_path = generate_character_video(
            text=text,
            character_id=character_id,
            voice_id=voice_id,
            output_path=output_path
        )
        
        if not video_path:
            return jsonify({"error": "Failed to generate video with Hedra API"}), 500
        
        # Create a URL for the video
        video_url = url_for('static', filename=f"videos/{filename}")
        
        return jsonify({
            "video_url": video_url,
            "text": text
        })
    
    except Exception as e:
        current_app.logger.error(f"Error generating video: {e}")
        return jsonify({"error": str(e)}), 500

@hedra_character_bp.route("/characters", methods=["GET"])
def get_characters():
    """
    Get a list of available characters from the Hedra API.
    
    Returns:
    {
        "characters": [
            {
                "id": "character_id",
                "name": "Character Name",
                "thumbnail_url": "URL to character thumbnail"
            },
            ...
        ]
    }
    """
    try:
        characters = list_characters()
        
        if not characters:
            return jsonify({"error": "Failed to get characters from Hedra API"}), 500
        
        return jsonify({"characters": characters})
    
    except Exception as e:
        current_app.logger.error(f"Error getting characters: {e}")
        return jsonify({"error": str(e)}), 500

@hedra_character_bp.route("/voices", methods=["GET"])
def get_voices():
    """
    Get a list of available voices from the Hedra API.
    
    Returns:
    {
        "voices": [
            {
                "id": "voice_id",
                "name": "Voice Name",
                "gender": "male/female",
                "language": "en-US"
            },
            ...
        ]
    }
    """
    try:
        voices = list_voices()
        
        if not voices:
            return jsonify({"error": "Failed to get voices from Hedra API"}), 500
        
        return jsonify({"voices": voices})
    
    except Exception as e:
        current_app.logger.error(f"Error getting voices: {e}")
        return jsonify({"error": str(e)}), 500
