"""
Minocrisy AI Tools - xAI (Grok) API Utilities
Utilities for interacting with the xAI API.
"""
import requests
import json
from flask import current_app
from app.utils.secrets import get_xai_api_key, get_xai_api_url

def chat_completion(messages, model="grok-3", temperature=0.7, max_tokens=1000):
    """
    Generate a chat completion using the xAI API.
    
    Args:
        messages: A list of message objects with 'role' and 'content' keys.
        model: The model to use (default: "grok-3").
        temperature: Controls randomness (0-1).
        max_tokens: Maximum number of tokens to generate.
        
    Returns:
        The generated response as a string, or None if an error occurred.
    """
    api_key = get_xai_api_key()
    api_url = get_xai_api_url()
    
    if not api_key:
        current_app.logger.error("xAI API key not configured")
        return None
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(
            f"{api_url}/chat/completions",
            headers=headers,
            json=data,
            verify=False  # Disable SSL certificate verification
        )
        # Suppress InsecureRequestWarning
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        if response.status_code != 200:
            current_app.logger.error(f"xAI API error: {response.status_code} - {response.text}")
            return None
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    except Exception as e:
        current_app.logger.error(f"Error calling xAI API: {e}")
        return None

def generate_image(prompt, model="grok-image-1", size="1024x1024", quality="standard", n=1):
    """
    Generate an image using the xAI API.
    
    Args:
        prompt: The text prompt to generate an image from.
        model: The model to use (default: "grok-image-1").
        size: The size of the image (default: "1024x1024").
        quality: The quality of the image (default: "standard").
        n: The number of images to generate (default: 1).
        
    Returns:
        A list of image URLs, or None if an error occurred.
    """
    api_key = get_xai_api_key()
    api_url = get_xai_api_url()
    
    if not api_key:
        current_app.logger.error("xAI API key not configured")
        return None
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "n": n
    }
    
    try:
        response = requests.post(
            f"{api_url}/images/generations",
            headers=headers,
            json=data,
            verify=False  # Disable SSL certificate verification
        )
        
        if response.status_code != 200:
            current_app.logger.error(f"xAI API error: {response.status_code} - {response.text}")
            return None
        
        result = response.json()
        return [image["url"] for image in result["data"]]
    
    except Exception as e:
        current_app.logger.error(f"Error calling xAI API: {e}")
        return None
