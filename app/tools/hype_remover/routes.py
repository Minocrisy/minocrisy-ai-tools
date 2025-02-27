"""
Minocrisy AI Tools - Hype Remover Routes
Routes for the Hype Remover tool.
"""
from flask import request, jsonify, render_template, current_app
from app.tools.hype_remover import hype_remover_bp
from app.tools.hype_remover.service import remove_hype, store_feedback, research_topic, save_output, get_saved_outputs, get_saved_output, delete_saved_output, create_x_post, create_google_doc_content
from app.utils.secrets import get_openai_api_key, get_xai_api_key, get_gemini_api_key

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
        "use_xai": true/false (default: true),
        "use_gemini": true/false (default: false)
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
    gemini_api_key = get_gemini_api_key()
    
    # Get request data
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text input is required"}), 400
    
    text = data["text"]
    strength = data.get("strength", "moderate")
    custom_hype_terms = data.get("custom_hype_terms", [])
    context = data.get("context")
    use_xai = data.get("use_xai", True)
    use_gemini = data.get("use_gemini", False)
    
    # Check if appropriate API key is available
    if use_gemini:
        if not gemini_api_key:
            use_gemini = False
            if xai_api_key:
                use_xai = True
                current_app.logger.warning("Gemini API key not configured, falling back to xAI")
            elif openai_api_key:
                use_xai = False
                current_app.logger.warning("Gemini API key not configured, falling back to OpenAI")
            else:
                return jsonify({"error": "No API keys configured"}), 500
    elif use_xai and not xai_api_key:
        if gemini_api_key:
            use_gemini = True
            use_xai = False
            current_app.logger.warning("xAI API key not configured, falling back to Gemini")
        elif openai_api_key:
            use_xai = False
            current_app.logger.warning("xAI API key not configured, falling back to OpenAI")
        else:
            return jsonify({"error": "No API keys configured"}), 500
    elif not use_xai and not openai_api_key:
        if gemini_api_key:
            use_gemini = True
            current_app.logger.warning("OpenAI API key not configured, falling back to Gemini")
        elif xai_api_key:
            use_xai = True
            current_app.logger.warning("OpenAI API key not configured, falling back to xAI")
        else:
            return jsonify({"error": "No API keys configured"}), 500
    
    try:
        # Process the text to remove hype
        api_key = openai_api_key if not use_xai and not use_gemini else None
        result = remove_hype(
            text=text, 
            strength=strength, 
            custom_hype_terms=custom_hype_terms,
            context=context,
            api_key=api_key,
            use_xai=use_xai,
            use_gemini=use_gemini
        )
        
        return jsonify(result)
    
    except Exception as e:
        current_app.logger.error(f"Error removing hype: {e}")
        return jsonify({"error": str(e)}), 500

@hype_remover_bp.route("/research", methods=["POST"])
def research():
    """
    Research a topic and return information.
    
    Request JSON:
    {
        "topic": "Topic to research",
        "use_xai": true/false (default: true),
        "use_gemini": true/false (default: false)
    }
    
    Returns:
    {
        "topic": "Original topic",
        "summary": "A comprehensive summary of the topic",
        "key_points": ["Key point 1", "Key point 2", "Key point 3"],
        "sources": [
            {
                "title": "Source title",
                "url": "Source URL (if available)",
                "description": "Brief description of the source"
            }
        ]
    }
    """
    # Get API keys
    xai_api_key = get_xai_api_key()
    openai_api_key = get_openai_api_key()
    gemini_api_key = get_gemini_api_key()
    
    # Get request data
    data = request.get_json()
    if not data or "topic" not in data:
        return jsonify({"error": "Topic is required"}), 400
    
    topic = data["topic"]
    use_xai = data.get("use_xai", True)
    use_gemini = data.get("use_gemini", False)
    
    # Check if appropriate API key is available
    if use_gemini:
        if not gemini_api_key:
            use_gemini = False
            if xai_api_key:
                use_xai = True
                current_app.logger.warning("Gemini API key not configured, falling back to xAI")
            elif openai_api_key:
                use_xai = False
                current_app.logger.warning("Gemini API key not configured, falling back to OpenAI")
            else:
                return jsonify({"error": "No API keys configured"}), 500
    elif use_xai and not xai_api_key:
        if gemini_api_key:
            use_gemini = True
            use_xai = False
            current_app.logger.warning("xAI API key not configured, falling back to Gemini")
        elif openai_api_key:
            use_xai = False
            current_app.logger.warning("xAI API key not configured, falling back to OpenAI")
        else:
            return jsonify({"error": "No API keys configured"}), 500
    elif not use_xai and not openai_api_key:
        if gemini_api_key:
            use_gemini = True
            current_app.logger.warning("OpenAI API key not configured, falling back to Gemini")
        elif xai_api_key:
            use_xai = True
            current_app.logger.warning("OpenAI API key not configured, falling back to xAI")
        else:
            return jsonify({"error": "No API keys configured"}), 500
    
    try:
        # Research the topic
        api_key = openai_api_key if not use_xai and not use_gemini else None
        result = research_topic(
            topic=topic,
            api_key=api_key,
            use_xai=use_xai,
            use_gemini=use_gemini
        )
        
        return jsonify(result)
    
    except Exception as e:
        current_app.logger.error(f"Error researching topic: {e}")
        return jsonify({"error": str(e)}), 500

@hype_remover_bp.route("/save", methods=["POST"])
def save():
    """
    Save processed text to local memory.
    
    Request JSON:
    {
        "title": "Title for the saved output",
        "original_text": "Original text that was processed",
        "processed_text": "Text after hype removal",
        "source_url": "Optional source URL"
    }
    
    Returns:
    {
        "success": true/false,
        "message": "Success/error message",
        "output_id": "ID of the saved output"
    }
    """
    # Get request data
    data = request.get_json()
    if not data or "title" not in data or "original_text" not in data or "processed_text" not in data:
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    
    title = data["title"]
    original_text = data["original_text"]
    processed_text = data["processed_text"]
    source_url = data.get("source_url")
    
    try:
        # Save the output
        output_id = save_output(title, original_text, processed_text, source_url)
        
        return jsonify({
            "success": True,
            "message": "Output saved successfully",
            "output_id": output_id
        })
    
    except Exception as e:
        current_app.logger.error(f"Error saving output: {e}")
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@hype_remover_bp.route("/saved", methods=["GET"])
def saved():
    """
    Get all saved outputs for the current user.
    
    Returns:
    {
        "outputs": {
            "output_id": {
                "timestamp": "ISO timestamp",
                "title": "Title for the saved output",
                "original_text": "Original text that was processed",
                "processed_text": "Text after hype removal",
                "source_url": "Optional source URL"
            }
        }
    }
    """
    try:
        # Get saved outputs
        outputs = get_saved_outputs()
        
        return jsonify({
            "outputs": outputs
        })
    
    except Exception as e:
        current_app.logger.error(f"Error getting saved outputs: {e}")
        return jsonify({"error": str(e)}), 500

@hype_remover_bp.route("/saved/<output_id>", methods=["GET"])
def get_output(output_id):
    """
    Get a specific saved output.
    
    Returns:
    {
        "timestamp": "ISO timestamp",
        "title": "Title for the saved output",
        "original_text": "Original text that was processed",
        "processed_text": "Text after hype removal",
        "source_url": "Optional source URL"
    }
    """
    try:
        # Get the saved output
        output = get_saved_output(output_id)
        
        if output:
            return jsonify(output)
        else:
            return jsonify({"error": "Output not found"}), 404
    
    except Exception as e:
        current_app.logger.error(f"Error getting saved output: {e}")
        return jsonify({"error": str(e)}), 500

@hype_remover_bp.route("/saved/<output_id>", methods=["DELETE"])
def delete_output(output_id):
    """
    Delete a specific saved output.
    
    Returns:
    {
        "success": true/false,
        "message": "Success/error message"
    }
    """
    try:
        # Delete the saved output
        success = delete_saved_output(output_id)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Output deleted successfully"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Output not found"
            }), 404
    
    except Exception as e:
        current_app.logger.error(f"Error deleting saved output: {e}")
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@hype_remover_bp.route("/export/x", methods=["POST"])
def export_x():
    """
    Format text as an X (Twitter) post.
    
    Request JSON:
    {
        "text": "Text to format"
    }
    
    Returns:
    {
        "formatted_text": "Formatted text for X"
    }
    """
    # Get request data
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text is required"}), 400
    
    text = data["text"]
    
    try:
        # Format the text for X
        formatted_text = create_x_post(text)
        
        return jsonify({
            "formatted_text": formatted_text
        })
    
    except Exception as e:
        current_app.logger.error(f"Error formatting text for X: {e}")
        return jsonify({"error": str(e)}), 500

@hype_remover_bp.route("/export/google-doc", methods=["POST"])
def export_google_doc():
    """
    Format text as Google Doc content.
    
    Request JSON:
    {
        "title": "Title for the document",
        "text": "Text content",
        "source_url": "Optional source URL"
    }
    
    Returns:
    {
        "content": "Formatted content for Google Doc"
    }
    """
    # Get request data
    data = request.get_json()
    if not data or "title" not in data or "text" not in data:
        return jsonify({"error": "Title and text are required"}), 400
    
    title = data["title"]
    text = data["text"]
    source_url = data.get("source_url")
    
    try:
        # Format the content for Google Doc
        content = create_google_doc_content(title, text, source_url)
        
        return jsonify({
            "content": content
        })
    
    except Exception as e:
        current_app.logger.error(f"Error formatting content for Google Doc: {e}")
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
