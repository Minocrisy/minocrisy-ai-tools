"""
Minocrisy AI Tools - Secrets Management
Utilities for managing API keys and secrets.
"""
import os
from flask import current_app
from google.cloud import secretmanager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_secret(secret_name):
    """
    Get a secret from environment variables or Google Cloud Secret Manager.
    
    Args:
        secret_name: The name of the secret to retrieve.
        
    Returns:
        The secret value as a string, or None if not found.
    """
    # First, try to get the secret from environment variables
    secret_value = os.environ.get(secret_name)
    if secret_value:
        return secret_value
    
    # If not found in environment variables, try Google Cloud Secret Manager
    try:
        # Check if GCP project ID is set
        project_id = current_app.config.get("GCP_PROJECT_ID")
        if not project_id:
            return None
        
        # Create the Secret Manager client
        client = secretmanager.SecretManagerServiceClient()
        
        # Build the resource name of the secret version
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        
        # Access the secret version
        response = client.access_secret_version(request={"name": name})
        
        # Return the decoded payload
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        current_app.logger.error(f"Error retrieving secret {secret_name}: {e}")
        return None

def get_elevenlabs_api_key():
    """Get the ElevenLabs API key."""
    return get_secret("ELEVENLABS_API_KEY") or current_app.config.get("ELEVENLABS_API_KEY")

def get_elevenlabs_voice_id():
    """Get the ElevenLabs voice ID."""
    return get_secret("ELEVENLABS_VOICE_ID") or current_app.config.get("ELEVENLABS_VOICE_ID")

def get_openai_api_key():
    """Get the OpenAI API key."""
    return get_secret("OPENAI_API_KEY") or current_app.config.get("OPENAI_API_KEY")

def get_runwayml_api_key():
    """Get the RunwayML API key."""
    return get_secret("RUNWAYML_API_KEY") or current_app.config.get("RUNWAYML_API_KEY")

def get_xai_api_key():
    """Get the xAI API key."""
    return get_secret("XAI_API_KEY") or current_app.config.get("XAI_API_KEY")

def get_xai_api_url():
    """Get the xAI API URL."""
    return get_secret("XAI_API_URL") or current_app.config.get("XAI_API_URL")

def get_hedra_api_key():
    """Get the Hedra API key."""
    return get_secret("HEDRA_API_KEY") or current_app.config.get("HEDRA_API_KEY")

def get_hedra_api_url():
    """Get the Hedra API URL."""
    return get_secret("HEDRA_API_URL") or current_app.config.get("HEDRA_API_URL")
