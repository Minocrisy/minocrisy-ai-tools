"""
Minocrisy AI Tools - Google Gemini API Utilities
Utilities for interacting with the Google Gemini API.
"""
import google.generativeai as genai
from flask import current_app
from app.utils.secrets import get_gemini_api_key

# Simple in-memory storage for conversation history
_conversation_memory = {}

def initialize_gemini():
    """Initialize the Gemini API with the API key."""
    api_key = get_gemini_api_key()
    if not api_key:
        current_app.logger.error("Gemini API key not configured")
        return False
    
    genai.configure(api_key=api_key)
    return True

def generate_image(prompt, model="imagen-3.0-generate-002", aspect_ratio="1:1", n=1):
    """
    Generate an image using Google's Imagen 3 model via the Gemini API.
    
    Args:
        prompt: The text prompt to generate an image from.
        model: The model to use (default: "imagen-3.0-generate-002").
        aspect_ratio: The aspect ratio of the generated image (default: "1:1").
                      Options: "1:1", "3:4", "4:3", "9:16", "16:9"
        n: The number of images to generate (default: 1, max: 4).
        
    Returns:
        A list of image URLs, or None if an error occurred.
    """
    api_key = get_gemini_api_key()
    if not api_key:
        current_app.logger.error("Gemini API key not configured")
        return None
    
    try:
        # For now, let's return None since we're having import issues
        # We'll need to investigate the correct import structure for the latest SDK
        current_app.logger.warning("Imagen API integration is not yet fully implemented. Falling back to default image.")
        return None
        
        # The following code is commented out until we resolve the import issues
        """
        import google.generativeai as genai
        from google.generativeai import types
        import base64
        
        # Configure the client
        genai.configure(api_key=api_key)
        
        # Create a client
        client = genai.Client()
        
        # Generate images
        response = client.generate_images(
            model=model,
            prompt=prompt,
            number_of_images=min(n, 4),  # Maximum 4 images
            aspect_ratio=aspect_ratio,
        )
        
        # Process the response
        urls = []
        for image in response.images:
            # Convert image bytes to data URI
            base64_image = base64.b64encode(image.bytes).decode("utf-8")
            data_uri = f"data:image/png;base64,{base64_image}"
            urls.append(data_uri)
        
        if not urls:
            current_app.logger.error("No images generated by Imagen API")
            return None
        
        return urls
        """
    
    except Exception as e:
        current_app.logger.error(f"Error calling Imagen API: {e}")
        return None

def chat_completion(messages, model="gemini-1.5-flash", temperature=0.7, max_tokens=1000):
    """
    Generate a chat completion using the Gemini API.
    
    Args:
        messages: A list of message objects with 'role' and 'content' keys.
        model: The model to use (default: "gemini-1.5-flash").
               Options: "gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"
        temperature: Controls randomness (0-1).
        max_tokens: Maximum number of tokens to generate.
        
    Returns:
        The generated response as a string, or None if an error occurred.
    """
    if not initialize_gemini():
        return None
    
    try:
        # Configure generation parameters
        generation_config = {
            "temperature": temperature,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": max_tokens,
        }
        
        # Create a model instance
        model_instance = genai.GenerativeModel(model_name=model, generation_config=generation_config)
        
        # Convert messages to Gemini format
        gemini_messages = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            gemini_messages.append({"role": role, "content": msg["content"]})
        
        # Generate response
        chat = model_instance.start_chat(history=gemini_messages)
        response = chat.send_message(gemini_messages[-1]["content"])
        
        if response and hasattr(response, 'text'):
            return response.text
        
        current_app.logger.error("No text generated by Gemini API")
        return None
    
    except Exception as e:
        current_app.logger.error(f"Error calling Gemini API: {e}")
        return None

def get_conversation_memory(session_id):
    """Get conversation memory for a session."""
    if session_id not in _conversation_memory:
        _conversation_memory[session_id] = []
    return _conversation_memory[session_id]

def add_to_conversation_memory(session_id, role, content):
    """Add a message to conversation memory."""
    if session_id not in _conversation_memory:
        _conversation_memory[session_id] = []
    
    _conversation_memory[session_id].append({
        "role": role,
        "content": content
    })
    
    # Limit memory size to prevent excessive token usage
    if len(_conversation_memory[session_id]) > 20:
        _conversation_memory[session_id] = _conversation_memory[session_id][-20:]
