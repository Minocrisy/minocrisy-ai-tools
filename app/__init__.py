"""
Minocrisy AI Tools - App Package
Contains the Flask application factory and configuration.
"""
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app(test_config=None):
    """
    Application factory function.
    Creates and configures the Flask application.
    """
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Enable CORS
    CORS(app)
    
    # Set default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY", ""),
        ELEVENLABS_VOICE_ID=os.environ.get("ELEVENLABS_VOICE_ID", ""),
        OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY", ""),
        RUNWAYML_API_KEY=os.environ.get("RUNWAYML_API_KEY", ""),
        XAI_API_KEY=os.environ.get("XAI_API_KEY", ""),
        XAI_API_URL=os.environ.get("XAI_API_URL", "https://api.xai.com/v1"),
        HEDRA_API_KEY=os.environ.get("HEDRA_API_KEY", ""),
        HEDRA_API_URL=os.environ.get("HEDRA_API_URL", "https://api.hedra.com/v1"),
        GCP_PROJECT_ID=os.environ.get("GCP_PROJECT_ID", ""),
    )
    
    # Load test config if provided
    if test_config is not None:
        app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    from app.tools.talking_head import talking_head_bp
    app.register_blueprint(talking_head_bp, url_prefix="/tools/talking-head")
    
    from app.tools.hype_remover import hype_remover_bp
    app.register_blueprint(hype_remover_bp, url_prefix="/tools/hype-remover")
    
    # Register new tool blueprints if the APIs are configured
    if app.config.get("XAI_API_KEY"):
        from app.tools.xai_chat import xai_chat_bp
        app.register_blueprint(xai_chat_bp, url_prefix="/tools/xai-chat")
    
    if app.config.get("HEDRA_API_KEY"):
        from app.tools.hedra_character import hedra_character_bp
        app.register_blueprint(hedra_character_bp, url_prefix="/tools/hedra-character")
    
    # Health check endpoint
    @app.route("/health")
    def health_check():
        return {"status": "healthy"}
    
    return app
