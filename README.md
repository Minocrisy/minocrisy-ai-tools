# Minocrisy AI Tools

A modular Flask-based web application for AI tools like Talking Head and Hype Remover, integrating ElevenLabs for text-to-speech, OpenAI for language processing, and RunwayML for animation.

## Features

- **Talking Head Tool**: Generate animated talking head videos from text input using ElevenLabs for text-to-speech and RunwayML for animation. Supports multiple AI image generators including DALL-E, GPT-4o, Grok, and Gemini Flash 2.0.
- **Hype Remover Tool**: Remove exaggerated claims and marketing hype from text using multiple AI models including OpenAI, xAI's Grok, and Google's Gemini Flash 2.0.
- **Grok Chat Tool**: Chat with xAI's Grok model for intelligent conversations and assistance. Supports image and document uploads for visual analysis with Grok Vision.
- **Hedra Character Video Tool**: Generate character videos with synchronized speech using Hedra's API.
- **Modular Architecture**: Easily add new AI tools to the platform.
- **Secure API Key Management**: Store API keys in .env files for local development or Google Cloud Secret Manager for production.
- **Google Cloud App Engine Ready**: Configured for deployment on Google Cloud's App Engine free tier.

## Setup

### Prerequisites

- Python 3.11
- Nix package manager (for development environment)
- GitHub Codespaces (optional)
- API keys for:
  - ElevenLabs (for text-to-speech)
  - OpenAI (for language processing)
  - RunwayML (for animation)
  - xAI (for Grok chat, optional)
  - Google Gemini (for text and image generation, optional)
  - Hedra (for character video generation, optional)
- Google Cloud account (for deployment)

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/minocrisy-ai-tools.git
   cd minocrisy-ai-tools
   ```

2. Set up the development environment using Nix:
   ```bash
   nix-shell dev.nix
   ```

3. Create a `.env` file with your API keys:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

4. Run the application:
   ```bash
   python main.py
   ```

5. Open your browser and navigate to `http://localhost:8080`

### GitHub Codespaces

This repository is configured for GitHub Codespaces. When you create a new Codespace, the environment will be automatically set up with Python 3.11, Flask, and all required dependencies.

1. Create a new Codespace from the GitHub repository.
2. Add your API keys to the `.env` file.
3. Run the application:
   ```bash
   python main.py
   ```

## Project Structure

```
minocrisy-ai-tools/
├── app/                        # Main application package
│   ├── __init__.py             # Application factory
│   ├── routes.py               # Main routes
│   ├── static/                 # Static files (CSS, JS, images)
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   ├── templates/              # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── talking_head/
│   │   │   └── index.html
│   │   ├── hype_remover/
│   │   │   └── index.html
│   │   ├── xai_chat/
│   │   │   └── index.html
│   │   └── hedra_character/
│   │       └── index.html
│   ├── tools/                  # Tool modules
│   │   ├── __init__.py
│   │   ├── talking_head/       # Talking Head tool
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── service.py
│   │   │   └── README.md       # Tool-specific documentation
│   │   ├── hype_remover/       # Hype Remover tool
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── service.py
│   │   │   └── README.md       # Tool-specific documentation
│   │   ├── xai_chat/           # Grok Chat tool
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── README.md       # Tool-specific documentation
│   │   └── hedra_character/    # Hedra Character Video tool
│   │       ├── __init__.py
│   │       ├── routes.py
│   │       └── README.md       # Tool-specific documentation
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── secrets.py          # API key management
│       ├── openai_api.py       # OpenAI API utilities
│       ├── xai_api.py          # xAI API utilities
│       ├── gemini_api.py       # Google Gemini API utilities
│       └── hedra_api.py        # Hedra API utilities
├── main.py                     # Application entry point
├── dev.nix                     # Nix development environment
├── requirements.txt            # Python dependencies
├── app.yaml                    # Google Cloud App Engine configuration
├── env_variables.yaml.template # Template for environment variables
├── .env.example                # Example .env file
├── tests/                      # Test suite
│   ├── __init__.py
│   └── test_app.py             # Application tests
├── run_tests.py                # Test runner
└── README.md                   # This file
```

## Deployment to Google Cloud App Engine

1. Create a Google Cloud project and enable the App Engine API.

2. Create a copy of the environment variables template:
   ```bash
   cp env_variables.yaml.template env_variables.yaml
   # Edit env_variables.yaml with your actual API keys
   ```

3. Deploy the application:
   ```bash
   gcloud app deploy
   ```

4. Open the deployed application:
   ```bash
   gcloud app browse
   ```

## API Key Management

### Local Development

For local development, API keys are stored in a `.env` file at the root of the project. This file is not committed to source control.

### Production (Google Cloud)

For production deployment on Google Cloud, there are two options:

1. **env_variables.yaml**: Store API keys in this file, which is included by app.yaml but not committed to source control.

2. **Google Cloud Secret Manager**: For enhanced security, API keys can be stored in Google Cloud Secret Manager. The application will automatically check Secret Manager if a key is not found in environment variables.

## Tool Documentation

Each tool in the platform has its own detailed documentation in a README.md file within its directory. These tool-specific READMEs provide:

- Detailed feature descriptions
- How the tool works
- API requirements
- Implementation details (routes and service functions)
- Usage examples with code snippets
- Troubleshooting information

You can find the documentation for each tool here:
- [Talking Head Tool](app/tools/talking_head/README.md)
- [Hype Remover Tool](app/tools/hype_remover/README.md)
- [Grok Chat Tool](app/tools/xai_chat/README.md)
- [Hedra Character Video Tool](app/tools/hedra_character/README.md)

## Adding New Tools

To add a new tool to the platform:

1. Create a new directory in `app/tools/` for your tool.
2. Create the necessary files (`__init__.py`, `routes.py`, `service.py`, `README.md`).
3. Register the tool's blueprint in `app/__init__.py`.
4. Add a template in `app/templates/` for the tool's UI.
5. Update the main page to include a link to your new tool.
6. Add the tool to the navigation menu in `app/templates/base.html`.

## Troubleshooting

### Missing Dependencies

If you encounter missing dependencies, ensure you're using the Nix development environment:

```bash
nix-shell dev.nix
```

Or install the dependencies manually:

```bash
pip install -r requirements.txt
```

### Nix Errors

If you encounter errors with Nix, ensure you have the latest version installed:

```bash
curl -L https://nixos.org/nix/install | sh
```

### Google Cloud IAM Permissions

If you encounter permission issues when deploying to Google Cloud, ensure your account has the necessary roles:

- App Engine Admin
- Cloud Build Editor
- Service Account User
- Storage Admin
- Secret Manager Admin (if using Secret Manager)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [ElevenLabs](https://elevenlabs.io/)
- [OpenAI](https://openai.com/)
- [RunwayML](https://runwayml.com/)
- [xAI](https://xai.com/)
- [Hedra](https://hedra.com/)
- [Google Cloud](https://cloud.google.com/)
- [Google Gemini](https://ai.google.dev/)
