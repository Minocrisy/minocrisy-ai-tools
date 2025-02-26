# Minimal development environment for Minocrisy AI Tools (Flask UI)
# Maintained at: ~/minocrisy-ai-tools/dev.nix
# Last updated: 2025
# Purpose: Simple AI and web development for Flask-based UI on Google Cloud
let
  pkgs = import <nixpkgs> {};
{
  channel = "stable-24.05";  # Use latest stable for reliability

  packages = with pkgs; [
    python311  # Python 3.11 for stability and compatibility
    python311Packages.pip  # For installing Python packages in Nix environment
    python311Packages.flask  # For the web server hosting the UI
    python311Packages.requests  # For API calls to xAI, ElevenLabs, etc.
    python311Packages.python-dotenv  # For loading environment variables from .env file
    python311Packages.gunicorn  # For production deployment on App Engine
    python311Packages.flask-cors  # For handling CORS in API requests
    python311Packages.google-cloud-secret-manager  # For Google Cloud Secret Manager
    python311Packages.google-auth  # For Google Cloud authentication
    python311Packages.pillow  # For image processing
    python311Packages.numpy  # For numerical operations
    python311Packages.pytest  # For testing
    python311Packages.black  # For code formatting
    python311Packages.flake8  # For linting
  ];

  env = {
    # Editor & Terminal settings (minimal for now)
    EDITOR = "code";
    TERM = "xterm-256color";

    # API Keys & Credentials for Minocrisy Tools (replace with your actual keys locally)
    XAI_API_KEY = "";  # Primary API key for xAI (Grok 3) – add your key
    XAI_API_URL = "https://api.xai.com/v1";  # xAI API endpoint
    ELEVENLABS_API_KEY = "";  # For ElevenLabs TTS – add your key
    ELEVENLABS_VOICE_ID = "";  # Voice ID from ElevenLabs (e.g., "Rachel") – add your chosen voice ID
    OPENAI_API_KEY = "";  # For OpenAI (DALL-E) – add your key
    RUNWAYML_API_KEY = "";  # For RunwayML animation – add your key
    HEDRA_API_KEY = "";  # For Hedra.com API – add your key
    HEDRA_API_URL = "https://api.hedra.com/v1";  # Hedra API endpoint
  };

  # Codespaces specific configurations
  idx = {
    extensions = [
      "ms-python.python"  # Essential for Python 3.11 development
      "ms-python.vscode-pylance"  # Python language server
      "ms-python.black-formatter"  # Code formatting
      "ms-python.flake8"  # Linting
      "ms-azuretools.vscode-docker"  # Docker support
      "googlecloudtools.cloudcode"  # Google Cloud integration
      "redhat.vscode-yaml"  # YAML support for app.yaml
      "ms-vscode.live-server"  # Live preview for web development
      "github.copilot"  # AI assistance (optional)
      "eamodio.gitlens"  # Git integration
    ];

    workspace = {
      onCreate = {
        setup-check = ''
          echo "🔧 Setting up Minocrisy AI Tools environment..."
          python3 --version  # Should show Python 3.11
          
          # Create project structure if it doesn't exist
          mkdir -p app/static app/templates app/tools/talking_head app/tools/hype_remover app/utils
          
          # Create .env file if it doesn't exist
          if [ ! -f .env ]; then
            echo "Creating .env file for local development..."
            cat > .env << EOL
# Minocrisy AI Tools - Environment Variables
# Replace with your actual API keys for local development

# ElevenLabs API (Text-to-Speech)
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=your_voice_id

# OpenAI API (Image Generation)
OPENAI_API_KEY=your_openai_api_key

# RunwayML API (Animation)
RUNWAYML_API_KEY=your_runwayml_api_key

# Google Cloud Project ID (for Secret Manager)
GCP_PROJECT_ID=your_gcp_project_id
EOL
          fi
          
          # Create requirements.txt if it doesn't exist
          if [ ! -f requirements.txt ]; then
            echo "Creating requirements.txt..."
            cat > requirements.txt << EOL
Flask==2.3.3
python-dotenv==1.0.0
requests==2.31.0
gunicorn==21.2.0
flask-cors==4.0.0
google-cloud-secret-manager==2.16.1
google-auth==2.22.0
Pillow==10.0.0
numpy==1.24.3
pytest==7.4.0
black==23.7.0
flake8==6.1.0
EOL
          fi
          
          # Create .gitignore if it doesn't exist
          if [ ! -f .gitignore ]; then
            echo "Creating .gitignore..."
            cat > .gitignore << EOL
# Environment variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Google Cloud
app.yaml
*.yaml.bak
credentials.json

# Logs
logs/
*.log
EOL
          fi
        '';
      };

      onStart = {
        environment-check = ''
          echo "🔍 Checking Minocrisy AI Tools environment..."
          echo "Python Version:"
          echo "=============="
          python3 --version
          
          echo "Installed Packages:"
          echo "=================="
          pip list | grep -E 'flask|requests|dotenv|google-cloud|pillow|numpy'
          
          echo "Project Structure:"
          echo "================="
          find . -type d -not -path "*/\.*" | sort
          
          echo "Environment Variables:"
          echo "===================="
          if [ -f .env ]; then
            echo "✅ .env file exists"
          else
            echo "❌ .env file missing"
          fi
          
          echo "Google Cloud Setup:"
          echo "================="
          if [ -f app.yaml ]; then
            echo "✅ app.yaml exists"
          else
            echo "❌ app.yaml missing (will be created during setup)"
          fi
        '';
      };
    };

    # Enable previews for Flask web server
    previews = {
      enable = true;
      previews = {
        web = {
          command = [ "python main.py" ];  # Run the Flask app directly
          env = { PORT = "$PORT"; };  # Use Codespaces' dynamic port (default 8080)
          manager = "web";
        };
      };
    };
  };
}
