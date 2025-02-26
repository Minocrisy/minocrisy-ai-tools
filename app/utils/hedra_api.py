"""
Minocrisy AI Tools - Hedra API Utilities
Utilities for interacting with the Hedra API for character video generation.
"""
import os
import requests
import json
import tempfile
from flask import current_app
from app.utils.secrets import get_hedra_api_key, get_hedra_api_url

def generate_character_video(text, character_id=None, voice_id=None, output_path=None):
    """
    Generate a character video using the Hedra API.
    
    Args:
        text: The text for the character to speak.
        character_id: The ID of the character to use (optional).
        voice_id: The ID of the voice to use (optional).
        output_path: The path to save the video file (optional).
        
    Returns:
        The path to the generated video file, or None if an error occurred.
    """
    api_key = get_hedra_api_key()
    api_url = get_hedra_api_url()
    
    if not api_key:
        current_app.logger.error("Hedra API key not configured")
        return None
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "text": text
    }
    
    if character_id:
        data["character_id"] = character_id
    
    if voice_id:
        data["voice_id"] = voice_id
    
    try:
        response = requests.post(
            f"{api_url}/generate",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            current_app.logger.error(f"Hedra API error: {response.status_code} - {response.text}")
            return None
        
        # If no output path is provided, create a temporary file
        if not output_path:
            temp_dir = tempfile.mkdtemp()
            output_path = os.path.join(temp_dir, "hedra_video.mp4")
        
        # Save the video file
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        return output_path
    
    except Exception as e:
        current_app.logger.error(f"Error calling Hedra API: {e}")
        return None

def list_characters():
    """
    Get a list of available characters from the Hedra API.
    
    Returns:
        A list of characters, or None if an error occurred.
    """
    api_key = get_hedra_api_key()
    api_url = get_hedra_api_url()
    
    if not api_key:
        current_app.logger.error("Hedra API key not configured")
        return None
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(
            f"{api_url}/characters",
            headers=headers
        )
        
        if response.status_code != 200:
            current_app.logger.error(f"Hedra API error: {response.status_code} - {response.text}")
            return None
        
        return response.json()
    
    except Exception as e:
        current_app.logger.error(f"Error calling Hedra API: {e}")
        return None

def list_voices():
    """
    Get a list of available voices from the Hedra API.
    
    Returns:
        A list of voices, or None if an error occurred.
    """
    api_key = get_hedra_api_key()
    api_url = get_hedra_api_url()
    
    if not api_key:
        current_app.logger.error("Hedra API key not configured")
        return None
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(
            f"{api_url}/voices",
            headers=headers
        )
        
        if response.status_code != 200:
            current_app.logger.error(f"Hedra API error: {response.status_code} - {response.text}")
            return None
        
        return response.json()
    
    except Exception as e:
        current_app.logger.error(f"Error calling Hedra API: {e}")
        return None
