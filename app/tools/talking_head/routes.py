"""
Minocrisy AI Tools - Talking Head Routes
Routes for the Talking Head tool.
"""
import os
import tempfile
import uuid
from flask import request, jsonify, current_app, render_template, url_for
from werkzeug.utils import secure_filename
from app.tools.talking_head import talking_head_bp
from app.tools.talking_head.service import generate_audio, generate_talking_head, generate_image
from app.utils.openai_api import download_image
from app.utils.secrets import get_elevenlabs_api_key, get_elevenlabs_voice_id, get_runwayml_api_key, get_openai_api_key, get_xai_api_key

@talking_head_bp.route("/", methods=["GET"])
def index():
    """Render the Talking Head tool page."""
    # Create directories for storing images and videos if they don't exist
    images_dir = os.path.join(current_app.static_folder, "images")
    videos_dir = os.path.join(current_app.static_folder, "videos")
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(videos_dir, exist_ok=True)
    
    return render_template("talking_head/index.html")

@talking_head_bp.route("/generate-image", methods=["POST"])
def generate_image_route():
    """
    Generate an image using the specified AI image generator.
    
    Request JSON:
    {
        "image_generator": "Image generator (default, dalle, gpt4o, xai)",
        "image_model": "Optional specific model for the selected generator",
        "image_prompt": "Prompt for generating the face image"
    }
    
    Returns:
    {
        "image_url": "URL of the generated image",
        "image_id": "Unique ID for the generated image"
    }
    """
    # Get API keys
    openai_api_key = get_openai_api_key()
    xai_api_key = get_xai_api_key()
    
    # Get request data
    data = request.get_json()
    if not data or "image_prompt" not in data:
        return jsonify({"error": "Image prompt is required"}), 400
    
    image_generator = data.get("image_generator", "default")
    image_model = data.get("image_model")
    image_prompt = data["image_prompt"]
    
    # Check if the requested image generator is available
    if image_generator == "dalle" and not openai_api_key:
        return jsonify({"error": "OpenAI API key not configured for DALL-E image generation"}), 500
    if image_generator == "gpt4o" and not openai_api_key:
        return jsonify({"error": "OpenAI API key not configured for GPT-4o image generation"}), 500
    if image_generator == "xai" and not xai_api_key:
        return jsonify({"error": "xAI API key not configured for Grok image generation"}), 500
    
    try:
        # Generate a unique ID for this request
        image_id = str(uuid.uuid4())
        
        # Generate the image
        image_url = generate_image(
            image_prompt, 
            generator=image_generator, 
            model=image_model, 
            as_data_uri=True
        )
        
        # Create images directory if it doesn't exist
        images_dir = os.path.join(current_app.static_folder, "images")
        os.makedirs(images_dir, exist_ok=True)
        
        # Save the image to a permanent location
        image_filename = f"{image_id}.jpg"
        permanent_image_path = os.path.join(images_dir, image_filename)
        
        # Extract image data from data URI if needed
        if image_url.startswith("data:"):
            import base64
            try:
                header, encoded = image_url.split(",", 1)
                image_data = base64.b64decode(encoded)
                with open(permanent_image_path, "wb") as f:
                    f.write(image_data)
            except Exception as e:
                current_app.logger.error(f"Error saving image from data URI: {e}")
                return jsonify({"error": f"Error saving image: {str(e)}"}), 500
        else:
            # Download and save the image
            image_data = download_image(image_url)
            if image_data:
                with open(permanent_image_path, "wb") as f:
                    f.write(image_data)
            else:
                return jsonify({"error": "Failed to download image"}), 500
        
        # Generate URL for the saved image
        display_image_url = url_for("static", filename=f"images/{image_filename}")
        
        return jsonify({
            "image_url": display_image_url,
            "image_id": image_id
        })
    
    except Exception as e:
        current_app.logger.error(f"Error generating image: {e}")
        return jsonify({"error": str(e)}), 500

@talking_head_bp.route("/upload-image", methods=["POST"])
def upload_image():
    """
    Upload an image to use as the face for the talking head.
    
    Returns:
    {
        "image_url": "URL of the uploaded image",
        "image_id": "Unique ID for the uploaded image"
    }
    """
    try:
        # Check if the post request has the file part
        if 'image' not in request.files:
            return jsonify({"error": "No image part in the request"}), 400
        
        file = request.files['image']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        # Generate a unique ID for this upload
        image_id = str(uuid.uuid4())
        
        # Create images directory if it doesn't exist
        images_dir = os.path.join(current_app.static_folder, "images")
        os.makedirs(images_dir, exist_ok=True)
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        extension = os.path.splitext(filename)[1].lower()
        if extension not in ['.jpg', '.jpeg', '.png', '.gif']:
            return jsonify({"error": "Invalid file format. Only JPG, PNG, and GIF are allowed."}), 400
        
        image_filename = f"{image_id}{extension}"
        file_path = os.path.join(images_dir, image_filename)
        file.save(file_path)
        
        # Generate URL for the saved image
        image_url = url_for("static", filename=f"images/{image_filename}")
        
        return jsonify({
            "image_url": image_url,
            "image_id": image_id
        })
    
    except Exception as e:
        current_app.logger.error(f"Error uploading image: {e}")
        return jsonify({"error": str(e)}), 500

@talking_head_bp.route("/gallery", methods=["GET"])
def gallery():
    """Get a list of all generated videos and images."""
    try:
        # Get all videos
        videos_dir = os.path.join(current_app.static_folder, "videos")
        os.makedirs(videos_dir, exist_ok=True)
        videos = []
        for filename in os.listdir(videos_dir):
            if filename.endswith('.mp4'):
                video_url = url_for("static", filename=f"videos/{filename}")
                videos.append({
                    "url": video_url,
                    "id": os.path.splitext(filename)[0],
                    "timestamp": os.path.getmtime(os.path.join(videos_dir, filename))
                })
        
        # Get all images
        images_dir = os.path.join(current_app.static_folder, "images")
        os.makedirs(images_dir, exist_ok=True)
        images = []
        for filename in os.listdir(images_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_url = url_for("static", filename=f"images/{filename}")
                images.append({
                    "url": image_url,
                    "id": os.path.splitext(filename)[0],
                    "timestamp": os.path.getmtime(os.path.join(images_dir, filename))
                })
        
        # Sort by timestamp (newest first)
        videos.sort(key=lambda x: x["timestamp"], reverse=True)
        images.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return jsonify({
            "videos": videos,
            "images": images
        })
    
    except Exception as e:
        current_app.logger.error(f"Error getting gallery: {e}")
        return jsonify({"error": str(e)}), 500

@talking_head_bp.route("/generate", methods=["POST"])
def generate():
    """
    Generate a talking head video from text input.
    
    Request JSON:
    {
        "text": "Text to convert to speech and animate",
        "voice_id": "Optional voice ID (defaults to configured voice)",
        "image_generator": "Optional image generator (default, dalle, gpt4o, xai)",
        "image_model": "Optional specific model for the selected generator",
        "image_prompt": "Optional prompt for generating the face image"
    }
    
    Returns:
    {
        "video_url": "URL to the generated video",
        "text": "Original text input",
        "image_url": "URL of the generated image (if applicable)"
    }
    """
    # Get API keys
    elevenlabs_api_key = get_elevenlabs_api_key()
    elevenlabs_voice_id = get_elevenlabs_voice_id()
    runwayml_api_key = get_runwayml_api_key()
    openai_api_key = get_openai_api_key()
    xai_api_key = get_xai_api_key()
    
    # Check if API keys are available
    if not elevenlabs_api_key:
        return jsonify({"error": "ElevenLabs API key not configured"}), 500
    if not runwayml_api_key:
        return jsonify({"error": "RunwayML API key not configured"}), 500
    
    # Get request data
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text input is required"}), 400
    
    text = data["text"]
    voice_id = data.get("voice_id", elevenlabs_voice_id)
    
    # Image generation options
    image_generator = data.get("image_generator", "default")
    image_model = data.get("image_model")
    image_prompt = data.get("image_prompt", "A professional person speaking to the camera")
    
    # Check if the requested image generator is available
    if image_generator == "dalle" and not openai_api_key:
        return jsonify({"error": "OpenAI API key not configured for DALL-E image generation"}), 500
    if image_generator == "gpt4o" and not openai_api_key:
        return jsonify({"error": "OpenAI API key not configured for GPT-4o image generation"}), 500
    if image_generator == "xai" and not xai_api_key:
        return jsonify({"error": "xAI API key not configured for Grok image generation"}), 500
    
    try:
        # Generate a unique ID for this request
        request_id = str(uuid.uuid4())
        
        # Create temporary directory for files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate audio from text using ElevenLabs
            audio_path = os.path.join(temp_dir, f"{request_id}.mp3")
            generate_audio(text, audio_path, voice_id, elevenlabs_api_key)
            
            # Generate or get the face image
            image_url = None
            if image_generator != "default":
                # Generate an image using the specified generator and get it as a data URI
                image_url = generate_image(
                    image_prompt, 
                    generator=image_generator, 
                    model=image_model, 
                    as_data_uri=True
                )
                
                # Also save the image for display in the UI
                image_path = os.path.join(temp_dir, f"{request_id}.jpg")
                image_data = download_image(image_url) if not image_url.startswith("data:") else None
                if not image_data and image_url.startswith("data:"):
                    # Extract image data from data URI
                    import base64
                    header, encoded = image_url.split(",", 1)
                    image_data = base64.b64decode(encoded)
                
                if image_data:
                    with open(image_path, "wb") as f:
                        f.write(image_data)
            
            # Generate talking head video using RunwayML
            video_path = os.path.join(temp_dir, f"{request_id}.mp4")
            
            # If image_url is a local URL (from our server), we need to convert it to a data URI
            if image_url and '/static/' in image_url:
                # Get the local file path
                local_path = os.path.join(current_app.static_folder, image_url.split('/static/')[1])
                if os.path.exists(local_path):
                    # Read the file and convert to data URI
                    with open(local_path, 'rb') as f:
                        import base64
                        import mimetypes
                        image_data = f.read()
                        mime_type = mimetypes.guess_type(local_path)[0] or "image/jpeg"
                        base64_image = base64.b64encode(image_data).decode("utf-8")
                        image_url = f"data:{mime_type};base64,{base64_image}"
            
            generate_talking_head(audio_path, video_path, runwayml_api_key, image_url)
            
            # Save the video to a permanent location
            output_dir = os.path.join(current_app.static_folder, "videos")
            os.makedirs(output_dir, exist_ok=True)
            
            output_filename = f"{request_id}.mp4"
            output_path = os.path.join(output_dir, output_filename)
            
            # Copy the video to the output directory
            with open(video_path, "rb") as src_file:
                with open(output_path, "wb") as dst_file:
                    dst_file.write(src_file.read())
            
            # Generate the URL for the video
            video_url = url_for("static", filename=f"videos/{output_filename}")
            
            # Prepare response
            response_data = {
                "video_url": video_url,
                "text": text
            }
            
            # Add image URL to response if an image was generated
            if image_generator != "default" and image_url:
                # Create images directory if it doesn't exist
                images_dir = os.path.join(current_app.static_folder, "images")
                os.makedirs(images_dir, exist_ok=True)
                
                # Save the image to a permanent location
                image_filename = f"{request_id}.jpg"
                permanent_image_path = os.path.join(images_dir, image_filename)
                
                # Extract image data from data URI if needed
                if image_url.startswith("data:"):
                    import base64
                    try:
                        header, encoded = image_url.split(",", 1)
                        image_data = base64.b64decode(encoded)
                        with open(permanent_image_path, "wb") as f:
                            f.write(image_data)
                    except Exception as e:
                        current_app.logger.error(f"Error saving image from data URI: {e}")
                elif os.path.exists(os.path.join(temp_dir, f"{request_id}.jpg")):
                    # Copy from temp directory
                    with open(os.path.join(temp_dir, f"{request_id}.jpg"), "rb") as src_file:
                        with open(permanent_image_path, "wb") as dst_file:
                            dst_file.write(src_file.read())
                
                # Generate URL for the saved image
                display_image_url = url_for("static", filename=f"images/{image_filename}")
                response_data["image_url"] = display_image_url
            
            return jsonify(response_data)
    
    except Exception as e:
        current_app.logger.error(f"Error generating talking head: {e}")
        return jsonify({"error": str(e)}), 500
