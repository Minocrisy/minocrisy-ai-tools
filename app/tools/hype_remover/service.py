"""
Minocrisy AI Tools - Hype Remover Service
Implementation of the Hype Remover tool functionality.
"""
import json
from flask import current_app
from app.utils.xai_api import chat_completion

def remove_hype(text, strength="moderate", custom_hype_terms=None, context=None, api_key=None, use_xai=True):
    """
    Remove hype and exaggerated claims from text using xAI or OpenAI API.
    
    Args:
        text: The text to process.
        strength: The strength of hype removal (mild, moderate, strong).
        custom_hype_terms: Optional list of custom terms or phrases to identify as hype.
        context: Optional context about the text to improve accuracy.
        api_key: The API key (not used when use_xai is True).
        use_xai: Whether to use xAI API instead of OpenAI API.
        
    Returns:
        A dictionary containing the original text, processed text, changes made, and confidence scores.
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
    
    # Add custom hype terms to the system prompt if provided
    if custom_hype_terms and len(custom_hype_terms) > 0:
        terms_list = ", ".join([f'"{term}"' for term in custom_hype_terms])
        system_prompt += f"\n\nPay special attention to the following terms or phrases that should be considered as hype: {terms_list}."
    
    # Add context to the system prompt if provided
    if context:
        system_prompt += f"\n\nContext about the text: {context}\nUse this context to better understand the domain and ensure you don't remove legitimate terminology or claims that are factual within this context."
    
    # Prepare the user message
    user_message = f"""Process the following text to remove hype and exaggerated claims according to the guidelines. 
    Return a JSON object with the following structure:
    {{
        "processed_text": "The text with hype removed",
        "changes": [
            {{
                "original": "Original phrase",
                "replacement": "Replacement phrase",
                "reason": "Reason for replacement",
                "confidence": 0.95 // A number between 0 and 1 indicating your confidence in this change
            }}
        ],
        "overall_hype_score": 0.75, // A number between 0 and 1 indicating the overall level of hype in the original text
        "accuracy_score": 0.9 // A number between 0 and 1 indicating your confidence in the accuracy of the processed text
    }}
    
    Text to process:
    {text}"""
    
    # Prepare the messages
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
    
    try:
        if use_xai:
            # Use xAI API
            content = chat_completion(
                messages=messages,
                model="grok-2-1212",  # Use available model
                temperature=0.2,  # Lower temperature for more consistent results
                max_tokens=4000   # Adjust based on expected response length
            )
            
            if not content:
                raise Exception("Failed to get response from xAI API")
            
            # Parse the response
            result = json.loads(content)
            
        else:
            # Use OpenAI API (legacy code path)
            import requests
            
            url = "https://api.openai.com/v1/chat/completions"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            data = {
                "model": "gpt-4-turbo",
                "messages": messages,
                "temperature": 0.2,
                "max_tokens": 2000,
                "response_format": {"type": "json_object"}
            }
            
            # Check if the model supports response_format
            if "gpt-4-turbo" not in data["model"] and "gpt-4-0125" not in data["model"] and "gpt-3.5-turbo-0125" not in data["model"]:
                # Remove response_format for models that don't support it
                data.pop("response_format", None)
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code != 200:
                error_message = f"OpenAI API error: {response.status_code} - {response.text}"
                current_app.logger.error(error_message)
                raise Exception(error_message)
            
            response_data = response.json()
            content = response_data["choices"][0]["message"]["content"]
            result = json.loads(content)
        
        # Add the original text to the result
        result["original_text"] = text
        
        # Ensure all changes have confidence scores
        for change in result.get("changes", []):
            if "confidence" not in change:
                change["confidence"] = 0.9  # Default confidence if not provided
        
        # Ensure overall scores are present
        if "overall_hype_score" not in result:
            result["overall_hype_score"] = 0.5  # Default hype score
        
        if "accuracy_score" not in result:
            result["accuracy_score"] = 0.9  # Default accuracy score
        
        return result
    
    except Exception as e:
        error_message = f"Error processing text: {e}"
        current_app.logger.error(error_message)
        raise Exception(error_message)

def store_feedback(original_text, processed_text, user_rating, user_comments=None):
    """
    Store user feedback on hype removal results for model improvement.
    
    Args:
        original_text: The original text that was processed.
        processed_text: The text after hype removal.
        user_rating: User rating (1-5) of the quality of hype removal.
        user_comments: Optional user comments about the results.
        
    Returns:
        True if feedback was successfully stored, False otherwise.
    """
    try:
        # In a production environment, this would store the feedback in a database
        # For now, we'll just log it
        feedback_data = {
            "original_text": original_text,
            "processed_text": processed_text,
            "user_rating": user_rating,
            "user_comments": user_comments
        }
        
        current_app.logger.info(f"User feedback received: {json.dumps(feedback_data)}")
        
        # TODO: In a real implementation, store this in a database for later analysis
        # and model improvement
        
        return True
    
    except Exception as e:
        current_app.logger.error(f"Error storing feedback: {e}")
        return False
