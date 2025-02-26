"""
Minocrisy AI Tools - Talking Head Routes
Routes for the Talking Head tool.
"""
import os
import tempfile
import uuid
from flask import request, jsonify, current_app, render_template, url_for
from werkzeug.utils import secure_filename
from app.tools.talking_head import talking_head_bp
from app.tools.talking_head.service import generate_audio, generate_talking_head
from app.utils.secrets import get_elevenlabs_api_key, get_elevenlabs_voice_id, get_runwayml_api_key

@talking_head_bp.route("/", methods=["GET"])
def index():
    """Render the Talking Head tool page."""
    return render_template("talking_head/index.html")

@talking_head_bp.route("/generate", methods=["POST"])
def generate():
    """
    Generate a talking head video from text input.
    
    Request JSON:
    {
        "text": "Text to convert to speech and animate",
        "voice_id": "Optional voice ID (defaults to configured voice)"
    }
    
    Returns:
    {
        "video_url": "URL to the generated video",
        "text": "Original text input"
    }
    """
    # Get API keys
    elevenlabs_api_key = get_elevenlabs_api_key()
    elevenlabs_voice_id = get_elevenlabs_voice_id()
    runwayml_api_key = get_runwayml_api_key()
    
    # Check if API keys are available
    if not elevenlabs_api_key:
        return jsonify({"error": "ElevenLabs API key not configured"}), 500
    if not runwayml_api_key:
        return jsonify({"error": "RunwayML API key not configured"}), 500
    
    # Get request data
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text input is required"}), 400
    
    text = data["text"]
    voice_id = data.get("voice_id", elevenlabs_voice_id)
    
    try:
        # Generate a unique ID for this request
        request_id = str(uuid.uuid4())
        
        # Create temporary directory for files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate audio from text using ElevenLabs
            audio_path = os.path.join(temp_dir, f"{request_id}.mp3")
            generate_audio(text, audio_path, voice_id, elevenlabs_api_key)
            
            # Generate talking head video using RunwayML
            video_path = os.path.join(temp_dir, f"{request_id}.mp4")
            generate_talking_head(audio_path, video_path, runwayml_api_key)
            
            # Save the video to a permanent location
            output_dir = os.path.join(current_app.static_folder, "videos")
            os.makedirs(output_dir, exist_ok=True)
            
            output_filename = f"{request_id}.mp4"
            output_path = os.path.join(output_dir, output_filename)
            
            # Copy the video to the output directory
            with open(video_path, "rb") as src_file:
                with open(output_path, "wb") as dst_file:
                    dst_file.write(src_file.read())
            
            # Generate the URL for the video
            video_url = url_for("static", filename=f"videos/{output_filename}")
            
            return jsonify({
                "video_url": video_url,
                "text": text
            })
    
    except Exception as e:
        current_app.logger.error(f"Error generating talking head: {e}")
        return jsonify({"error": str(e)}), 500
