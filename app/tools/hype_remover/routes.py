"""
Minocrisy AI Tools - Hype Remover Routes
Routes for the Hype Remover tool.
"""
from flask import request, jsonify, render_template, current_app
from app.tools.hype_remover import hype_remover_bp
from app.tools.hype_remover.service import remove_hype
from app.utils.secrets import get_openai_api_key

@hype_remover_bp.route("/", methods=["GET"])
def index():
    """Render the Hype Remover tool page."""
    return render_template("hype_remover/index.html")

@hype_remover_bp.route("/process", methods=["POST"])
def process():
    """
    Process text to remove hype and exaggerated claims.
    
    Request JSON:
    {
        "text": "Text to process",
        "strength": "Optional strength level (mild, moderate, strong)"
    }
    
    Returns:
    {
        "original_text": "Original text input",
        "processed_text": "Text with hype removed",
        "changes": [
            {
                "original": "Original phrase",
                "replacement": "Replacement phrase",
                "reason": "Reason for replacement"
            }
        ]
    }
    """
    # Get OpenAI API key
    openai_api_key = get_openai_api_key()
    
    # Check if API key is available
    if not openai_api_key:
        return jsonify({"error": "OpenAI API key not configured"}), 500
    
    # Get request data
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text input is required"}), 400
    
    text = data["text"]
    strength = data.get("strength", "moderate")
    
    try:
        # Process the text to remove hype
        result = remove_hype(text, strength, openai_api_key)
        
        return jsonify(result)
    
    except Exception as e:
        current_app.logger.error(f"Error removing hype: {e}")
        return jsonify({"error": str(e)}), 500
