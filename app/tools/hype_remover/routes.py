"""
Minocrisy AI Tools - Hype Remover Routes
Routes for the Hype Remover tool.
"""
from flask import request, jsonify, render_template, current_app
from app.tools.hype_remover import hype_remover_bp
from app.tools.hype_remover.service import remove_hype, store_feedback
from app.utils.secrets import get_openai_api_key, get_xai_api_key

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
        "strength": "Optional strength level (mild, moderate, strong)",
        "custom_hype_terms": ["Optional", "list", "of", "custom", "hype", "terms"],
        "context": "Optional context about the text",
        "use_xai": true/false (default: true)
    }
    
    Returns:
    {
        "original_text": "Original text input",
        "processed_text": "Text with hype removed",
        "changes": [
            {
                "original": "Original phrase",
                "replacement": "Replacement phrase",
                "reason": "Reason for replacement",
                "confidence": 0.95
            }
        ],
        "overall_hype_score": 0.75,
        "accuracy_score": 0.9
    }
    """
    # Get API keys
    xai_api_key = get_xai_api_key()
    openai_api_key = get_openai_api_key()
    
    # Get request data
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text input is required"}), 400
    
    text = data["text"]
    strength = data.get("strength", "moderate")
    custom_hype_terms = data.get("custom_hype_terms", [])
    context = data.get("context")
    use_xai = data.get("use_xai", True)
    
    # Check if appropriate API key is available
    if use_xai and not xai_api_key:
        if openai_api_key:
            # Fall back to OpenAI if xAI key is not available
            use_xai = False
            current_app.logger.warning("xAI API key not configured, falling back to OpenAI")
        else:
            return jsonify({"error": "No API keys configured"}), 500
    elif not use_xai and not openai_api_key:
        if xai_api_key:
            # Fall back to xAI if OpenAI key is not available
            use_xai = True
            current_app.logger.warning("OpenAI API key not configured, falling back to xAI")
        else:
            return jsonify({"error": "No API keys configured"}), 500
    
    try:
        # Process the text to remove hype
        api_key = openai_api_key if not use_xai else None
        result = remove_hype(
            text=text, 
            strength=strength, 
            custom_hype_terms=custom_hype_terms,
            context=context,
            api_key=api_key,
            use_xai=use_xai
        )
        
        return jsonify(result)
    
    except Exception as e:
        current_app.logger.error(f"Error removing hype: {e}")
        return jsonify({"error": str(e)}), 500

@hype_remover_bp.route("/feedback", methods=["POST"])
def feedback():
    """
    Store user feedback on hype removal results.
    
    Request JSON:
    {
        "original_text": "Original text that was processed",
        "processed_text": "Text after hype removal",
        "rating": 4, // User rating (1-5)
        "comments": "Optional user comments"
    }
    
    Returns:
    {
        "success": true/false,
        "message": "Success/error message"
    }
    """
    # Get request data
    data = request.get_json()
    if not data or "original_text" not in data or "processed_text" not in data or "rating" not in data:
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    
    original_text = data["original_text"]
    processed_text = data["processed_text"]
    rating = data["rating"]
    comments = data.get("comments")
    
    # Validate rating
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return jsonify({"success": False, "message": "Rating must be between 1 and 5"}), 400
    except ValueError:
        return jsonify({"success": False, "message": "Rating must be a number between 1 and 5"}), 400
    
    try:
        # Store the feedback
        success = store_feedback(original_text, processed_text, rating, comments)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Thank you for your feedback! It will help us improve the tool."
            })
        else:
            return jsonify({
                "success": False,
                "message": "Failed to store feedback. Please try again later."
            }), 500
    
    except Exception as e:
        current_app.logger.error(f"Error storing feedback: {e}")
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
