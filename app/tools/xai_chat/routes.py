"""
Minocrisy AI Tools - xAI Chat Routes
Routes for the xAI Chat tool.
"""
import json
from flask import request, jsonify, render_template, current_app, session
from app.tools.xai_chat import xai_chat_bp
from app.utils.xai_api import chat_completion
from app.utils.secrets import get_xai_api_key

@xai_chat_bp.route("/", methods=["GET"])
def index():
    """Render the xAI Chat tool page."""
    return render_template("xai_chat/index.html")

@xai_chat_bp.route("/chat", methods=["POST"])
def chat():
    """
    Process a chat message and get a response from the xAI API.
    
    Request JSON:
    {
        "message": "User's message",
        "conversation_id": "Optional conversation ID for continuing a conversation",
        "model": "Optional model name (defaults to grok-3)",
        "temperature": "Optional temperature value (0-1)"
    }
    
    Returns:
    {
        "response": "AI response",
        "conversation_id": "Conversation ID for continuing the conversation"
    }
    """
    # Get xAI API key
    xai_api_key = get_xai_api_key()
    
    # Check if API key is available
    if not xai_api_key:
        return jsonify({"error": "xAI API key not configured"}), 500
    
    # Get request data
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400
    
    message = data["message"]
    conversation_id = data.get("conversation_id")
    model = data.get("model", "grok-3")
    temperature = data.get("temperature", 0.7)
    
    try:
        # Get or create conversation history
        conversation_history = []
        
        if conversation_id and conversation_id in session:
            conversation_history = session[conversation_id]
        else:
            # Generate a new conversation ID if none provided or invalid
            conversation_id = str(hash(str(message) + str(current_app.config.get("SECRET_KEY"))))
            
            # Add system message to start the conversation
            conversation_history = [
                {
                    "role": "system",
                    "content": "You are Grok, a helpful AI assistant created by xAI. You are knowledgeable, friendly, and provide accurate information. You can help with a wide range of tasks, from answering questions to providing creative content."
                }
            ]
        
        # Add user message to conversation history
        conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # Get response from xAI API
        response = chat_completion(
            messages=conversation_history,
            model=model,
            temperature=float(temperature),
            max_tokens=1000
        )
        
        if not response:
            return jsonify({"error": "Failed to get response from xAI API"}), 500
        
        # Add assistant response to conversation history
        conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Store updated conversation history in session
        session[conversation_id] = conversation_history
        
        return jsonify({
            "response": response,
            "conversation_id": conversation_id
        })
    
    except Exception as e:
        current_app.logger.error(f"Error in xAI chat: {e}")
        return jsonify({"error": str(e)}), 500

@xai_chat_bp.route("/clear", methods=["POST"])
def clear_conversation():
    """
    Clear a conversation history.
    
    Request JSON:
    {
        "conversation_id": "Conversation ID to clear"
    }
    
    Returns:
    {
        "success": true/false
    }
    """
    # Get request data
    data = request.get_json()
    if not data or "conversation_id" not in data:
        return jsonify({"error": "Conversation ID is required"}), 400
    
    conversation_id = data["conversation_id"]
    
    try:
        # Remove conversation from session
        if conversation_id in session:
            session.pop(conversation_id)
        
        return jsonify({"success": True})
    
    except Exception as e:
        current_app.logger.error(f"Error clearing conversation: {e}")
        return jsonify({"error": str(e)}), 500
