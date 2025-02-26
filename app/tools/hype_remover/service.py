"""
Minocrisy AI Tools - Hype Remover Service
Implementation of the Hype Remover tool functionality.
"""
import json
import requests
from flask import current_app

def remove_hype(text, strength="moderate", api_key=None):
    """
    Remove hype and exaggerated claims from text using OpenAI API.
    
    Args:
        text: The text to process.
        strength: The strength of hype removal (mild, moderate, strong).
        api_key: The OpenAI API key.
        
    Returns:
        A dictionary containing the original text, processed text, and changes made.
    """
    # Define the system prompt based on the strength
    if strength == "mild":
        system_prompt = """You are a fact-checking assistant that identifies and tones down mild exaggerations and marketing hype in text. 
        Maintain the overall message but replace clearly exaggerated claims with more measured, factual statements. 
        Only modify phrases that contain obvious hype or exaggeration."""
    elif strength == "strong":
        system_prompt = """You are a rigorous fact-checking assistant that aggressively identifies and removes marketing hype, exaggerations, and unsubstantiated claims from text. 
        Replace all promotional language, superlatives, and exaggerated claims with strictly factual, neutral statements. 
        Be thorough in identifying and modifying any language that makes claims without evidence."""
    else:  # moderate (default)
        system_prompt = """You are a balanced fact-checking assistant that identifies and removes marketing hype and exaggerated claims from text. 
        Replace promotional language and exaggerated statements with more measured, factual alternatives. 
        Focus on modifying claims that lack substantiation or use excessive superlatives."""
    
    # Prepare the messages for the OpenAI API
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"""Process the following text to remove hype and exaggerated claims according to the guidelines. 
            Return a JSON object with the following structure:
            {{
                "processed_text": "The text with hype removed",
                "changes": [
                    {{
                        "original": "Original phrase",
                        "replacement": "Replacement phrase",
                        "reason": "Reason for replacement"
                    }}
                ]
            }}
            
            Text to process:
            {text}"""
        }
    ]
    
    # Call the OpenAI API
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "gpt-4",  # Use GPT-4 for better understanding of context and nuance
        "messages": messages,
        "temperature": 0.2,  # Lower temperature for more consistent results
        "max_tokens": 2000,  # Adjust based on expected response length
        "response_format": {"type": "json_object"}  # Request JSON response
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code != 200:
        error_message = f"OpenAI API error: {response.status_code} - {response.text}"
        current_app.logger.error(error_message)
        raise Exception(error_message)
    
    # Parse the response
    try:
        response_data = response.json()
        content = response_data["choices"][0]["message"]["content"]
        result = json.loads(content)
        
        # Add the original text to the result
        result["original_text"] = text
        
        return result
    
    except Exception as e:
        error_message = f"Error parsing OpenAI response: {e}"
        current_app.logger.error(error_message)
        raise Exception(error_message)
