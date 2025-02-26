"""
Minocrisy AI Tools - Talking Head Service
Implementation of the Talking Head tool functionality.
"""
import os
import requests
import json
import time
from flask import current_app

def generate_audio(text, output_path, voice_id, api_key):
    """
    Generate audio from text using ElevenLabs API.
    
    Args:
        text: The text to convert to speech.
        output_path: The path to save the audio file.
        voice_id: The ID of the voice to use.
        api_key: The ElevenLabs API key.
        
    Returns:
        The path to the generated audio file.
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code != 200:
        error_message = f"ElevenLabs API error: {response.status_code} - {response.text}"
        current_app.logger.error(error_message)
        raise Exception(error_message)
    
    # Save the audio file
    with open(output_path, "wb") as f:
        f.write(response.content)
    
    return output_path

def generate_talking_head(audio_path, output_path, api_key):
    """
    Generate a talking head video from an audio file using RunwayML API.
    
    Args:
        audio_path: The path to the audio file.
        output_path: The path to save the video file.
        api_key: The RunwayML API key.
        
    Returns:
        The path to the generated video file.
    """
    # RunwayML API endpoint for Gen-2 Lip Sync
    url = "https://api.runwayml.com/v1/generationJob"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Read the audio file
    with open(audio_path, "rb") as f:
        audio_data = f.read()
    
    # Create a generation job
    data = {
        "model": "lip-sync",
        "input": {
            "audio": {
                "data": audio_data.hex(),
                "mime_type": "audio/mpeg"
            },
            "image": {
                "url": "https://storage.googleapis.com/minocrisy-ai-tools/default_face.jpg"  # Default face image
            }
        },
        "webhook": None
    }
    
    # Start the generation job
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code != 200:
        error_message = f"RunwayML API error: {response.status_code} - {response.text}"
        current_app.logger.error(error_message)
        raise Exception(error_message)
    
    job_id = response.json().get("id")
    
    # Poll for job completion
    status_url = f"https://api.runwayml.com/v1/generationJob/{job_id}"
    
    max_attempts = 60  # 5 minutes (5 seconds * 60)
    attempts = 0
    
    while attempts < max_attempts:
        time.sleep(5)  # Wait 5 seconds between polls
        
        status_response = requests.get(status_url, headers=headers)
        
        if status_response.status_code != 200:
            error_message = f"RunwayML API error: {status_response.status_code} - {status_response.text}"
            current_app.logger.error(error_message)
            raise Exception(error_message)
        
        status_data = status_response.json()
        status = status_data.get("status")
        
        if status == "COMPLETED":
            # Download the video
            video_url = status_data.get("output", {}).get("video", {}).get("url")
            
            if not video_url:
                raise Exception("No video URL in RunwayML response")
            
            video_response = requests.get(video_url)
            
            if video_response.status_code != 200:
                error_message = f"Error downloading video: {video_response.status_code} - {video_response.text}"
                current_app.logger.error(error_message)
                raise Exception(error_message)
            
            # Save the video file
            with open(output_path, "wb") as f:
                f.write(video_response.content)
            
            return output_path
        
        elif status == "FAILED":
            error_message = f"RunwayML job failed: {status_data.get('error', 'Unknown error')}"
            current_app.logger.error(error_message)
            raise Exception(error_message)
        
        attempts += 1
    
    raise Exception("RunwayML job timed out")
