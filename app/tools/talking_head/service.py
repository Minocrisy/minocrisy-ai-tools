"""
Minocrisy AI Tools - Talking Head Service
Implementation of the Talking Head tool functionality.
"""
import os
import requests
import json
import time
import uuid
from flask import current_app
from app.utils.openai_api import generate_image_dalle, generate_image_gpt4o, download_image
from app.utils.xai_api import generate_image as generate_image_xai
from app.utils.gemini_api import generate_image as generate_image_gemini

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

def generate_image(prompt, generator="default", model=None, save_path=None, as_data_uri=False):
    """
    Generate an image using the specified AI image generator.
    
    Args:
        prompt: The text prompt to generate an image from.
        generator: The image generator to use (default: "default").
                   Options: "default", "dalle", "gpt4o", "xai"
        model: The specific model to use (optional, depends on generator).
        save_path: The path to save the image file (optional).
        as_data_uri: Whether to return the image as a data URI (default: False).
        
    Returns:
        The path to the saved image file, the image URL, or a data URI.
    """
    image_url = None
    
    try:
        if generator == "dalle":
            # Use DALL-E models
            dalle_model = model or "dall-e-3"
            urls = generate_image_dalle(prompt, model=dalle_model)
            if urls and len(urls) > 0:
                image_url = urls[0]
        
        elif generator == "gpt4o":
            # Use GPT-4o models
            gpt4o_model = model or "gpt-4o-mini"
            image_url = generate_image_gpt4o(prompt, model=gpt4o_model)
        
        elif generator == "xai":
            # Use xAI (Grok) models
            xai_model = model or "grok-image-1"
            urls = generate_image_xai(prompt, model=xai_model)
            if urls and len(urls) > 0:
                image_url = urls[0]
        
        # Gemini image generation is temporarily disabled due to API compatibility issues
        # elif generator == "gemini":
        #     # Use Gemini models
        #     gemini_model = model or "gemini-pro-vision"
        #     urls = generate_image_gemini(prompt, model=gemini_model)
        #     if urls and len(urls) > 0:
        #         image_url = urls[0]
        
        else:
            # Default to using a pre-defined image
            default_url = "https://storage.googleapis.com/minocrisy-ai-tools/default_face.jpg"
            if as_data_uri:
                # Convert default image to data URI
                image_data = download_image(default_url)
                if image_data:
                    import base64
                    base64_image = base64.b64encode(image_data).decode("utf-8")
                    return f"data:image/jpeg;base64,{base64_image}"
            return default_url
        
        if not image_url:
            current_app.logger.error(f"Failed to generate image with {generator}")
            default_url = "https://storage.googleapis.com/minocrisy-ai-tools/default_face.jpg"
            if as_data_uri:
                # Convert default image to data URI
                image_data = download_image(default_url)
                if image_data:
                    import base64
                    base64_image = base64.b64encode(image_data).decode("utf-8")
                    return f"data:image/jpeg;base64,{base64_image}"
            return default_url
        
        # If save_path is provided, download and save the image
        if save_path or as_data_uri:
            image_data = download_image(image_url)
            if image_data:
                if save_path:
                    with open(save_path, "wb") as f:
                        f.write(image_data)
                
                if as_data_uri:
                    import base64
                    import mimetypes
                    mime_type = mimetypes.guess_type(image_url)[0] or "image/jpeg"
                    base64_image = base64.b64encode(image_data).decode("utf-8")
                    return f"data:{mime_type};base64,{base64_image}"
                
                if save_path:
                    return save_path
        
        return image_url
    
    except Exception as e:
        current_app.logger.error(f"Error generating image: {e}")
        return "https://storage.googleapis.com/minocrisy-ai-tools/default_face.jpg"

def generate_talking_head(audio_path, output_path, api_key, image_url=None):
    """
    Generate a talking head video from an audio file using RunwayML API.
    
    Args:
        audio_path: The path to the audio file.
        output_path: The path to save the video file.
        api_key: The RunwayML API key.
        image_url: The URL of the image to use as the face (optional).
        
    Returns:
        The path to the generated video file.
    """
    # RunwayML API endpoint for Gen-3 Turbo
    url = "https://api.dev.runwayml.com/v1/image_to_video"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Runway-Version": "2024-11-06"
    }
    
    # Read the audio file
    with open(audio_path, "rb") as f:
        audio_data = f.read()
    
    # Use the provided image URL or default to the pre-defined image
    default_image_url = "https://storage.googleapis.com/minocrisy-ai-tools/default_face.jpg"
    if not image_url:
        image_url = default_image_url
    
    # Download the image and convert to base64 if it's a URL
    if not image_url.startswith("data:image/"):
        image_data = download_image(image_url)
        if image_data:
            import base64
            import mimetypes
            mime_type = mimetypes.guess_type(image_url)[0] or "image/jpeg"
            base64_image = base64.b64encode(image_data).decode("utf-8")
            image_url = f"data:{mime_type};base64,{base64_image}"
    
    # Create a generation job
    data = {
        "model": "gen3a_turbo",
        "promptImage": image_url,
        "promptText": "Generate a talking head video",
        "promptAudio": f"data:audio/mpeg;base64,{audio_data.hex()}"
    }
    
    # Start the generation job
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code != 200:
        error_message = f"RunwayML API error: {response.status_code} - {response.text}"
        current_app.logger.error(error_message)
        raise Exception(error_message)
    
    job_id = response.json().get("id")
    
    # Poll for job completion
    status_url = f"https://api.dev.runwayml.com/v1/image_to_video/{job_id}"
    
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
        
        if status == "SUCCEEDED":
            # Download the video
            video_url = status_data.get("result", {}).get("video")
            
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
