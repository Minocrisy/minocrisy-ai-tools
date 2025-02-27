"""
Minocrisy AI Tools - OpenAI API Utilities
Utilities for interacting with the OpenAI API.
"""
import requests
import json
import base64
from flask import current_app
from app.utils.secrets import get_openai_api_key

def generate_image_dalle(prompt, model="dall-e-3", size="1024x1024", quality="standard", n=1):
    """
    Generate an image using OpenAI's DALL-E models.
    
    Args:
        prompt: The text prompt to generate an image from.
        model: The model to use (default: "dall-e-3").
               Options: "dall-e-3", "dall-e-2"
        size: The size of the image (default: "1024x1024").
              Options for DALL-E 3: "1024x1024", "1792x1024", "1024x1792"
              Options for DALL-E 2: "256x256", "512x512", "1024x1024"
        quality: The quality of the image (default: "standard").
                 Options: "standard", "hd" (DALL-E 3 only)
        n: The number of images to generate (default: 1).
           DALL-E 3 only supports n=1
        
    Returns:
        A list of image URLs, or None if an error occurred.
    """
    api_key = get_openai_api_key()
    
    if not api_key:
        current_app.logger.error("OpenAI API key not configured")
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
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            current_app.logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
            return None
        
        result = response.json()
        return [image["url"] for image in result["data"]]
    
    except Exception as e:
        current_app.logger.error(f"Error calling OpenAI API: {e}")
        return None

def generate_image_gpt4o(prompt, model="gpt-4o-mini", size="1024x1024", quality="standard"):
    """
    Generate an image using OpenAI's GPT-4o models with vision capabilities.
    
    Args:
        prompt: The text prompt to generate an image from.
        model: The model to use (default: "gpt-4o-mini").
               Options: "gpt-4o", "gpt-4o-mini"
        size: The size of the image (default: "1024x1024").
        quality: The quality of the image (default: "standard").
        
    Returns:
        An image URL, or None if an error occurred.
    """
    api_key = get_openai_api_key()
    
    if not api_key:
        current_app.logger.error("OpenAI API key not configured")
        return None
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # GPT-4o uses the chat completions API with a specific format for image generation
    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are an AI assistant that generates images based on text prompts. Generate a detailed, high-quality image that matches the user's description."
            },
            {
                "role": "user",
                "content": f"Generate an image of: {prompt}"
            }
        ],
        "response_format": {"type": "image_url"}
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            current_app.logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
            return None
        
        result = response.json()
        # Extract the image URL from the response
        image_url = result["choices"][0]["message"]["content"]
        return image_url
    
    except Exception as e:
        current_app.logger.error(f"Error calling OpenAI API: {e}")
        return None

def download_image(url):
    """
    Download an image from a URL.
    
    Args:
        url: The URL of the image to download.
        
    Returns:
        The image data as bytes, or None if an error occurred.
    """
    try:
        response = requests.get(url)
        
        if response.status_code != 200:
            current_app.logger.error(f"Error downloading image: {response.status_code}")
            return None
        
        return response.content
    
    except Exception as e:
        current_app.logger.error(f"Error downloading image: {e}")
        return None
