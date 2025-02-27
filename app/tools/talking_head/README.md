# Talking Head Tool

The Talking Head tool generates animated talking head videos from text input using ElevenLabs for text-to-speech and RunwayML's gen3a_turbo model for animation. It supports generating custom face images using various AI image generators, uploading your own images, and maintains a gallery of all generated content.

## Features

- Convert text to natural-sounding speech using ElevenLabs API
- Animate a virtual presenter with lip-syncing using RunwayML API
- Generate custom face images using AI image generators:
  - DALL-E 3 and DALL-E 2 (OpenAI)
  - GPT-4o and GPT-4o Mini (OpenAI)
  - Grok (xAI) when available
  - Gemini Flash 2.0 (Google)
- Upload your own images to use as the talking head
- Preview and approve generated images before creating videos
- Browse a gallery of all generated images and videos
- Reuse previously generated or uploaded images for new videos
- Create engaging video content quickly and easily

## How It Works

1. The user enters text that they want the virtual presenter to speak
2. The text is sent to ElevenLabs API to generate natural-sounding speech audio
3. The audio file is sent to RunwayML API along with a presenter template to generate a synchronized talking head video
4. The resulting video is saved and presented to the user for download or embedding

## API Requirements

- **ElevenLabs API**: Used for text-to-speech conversion
  - Required environment variables:
    - `ELEVENLABS_API_KEY`: Your ElevenLabs API key
    - `ELEVENLABS_VOICE_ID`: The voice ID to use for speech generation

- **RunwayML API**: Used for video animation
  - Required environment variables:
    - `RUNWAYML_API_KEY`: Your RunwayML API key

- **OpenAI API** (Optional): Used for image generation with DALL-E and GPT-4o
  - Required environment variables:
    - `OPENAI_API_KEY`: Your OpenAI API key

- **xAI API** (Optional): Used for image generation with Grok
  - Required environment variables:
    - `XAI_API_KEY`: Your xAI API key
    - `XAI_API_URL`: The xAI API URL

- **Google Gemini API** (Optional): Used for image generation with Gemini Flash 2.0
  - Required environment variables:
    - `GEMINI_API_KEY`: Your Google Gemini API key

## Implementation Details

### Routes

- `GET /tools/talking-head/`: Renders the Talking Head tool interface
- `POST /tools/talking-head/generate`: Processes text input and generates a talking head video
- `POST /tools/talking-head/generate-image`: Generates an image using the specified AI image generator
- `POST /tools/talking-head/upload-image`: Uploads an image to use as the talking head
- `GET /tools/talking-head/gallery`: Returns a list of all generated videos and images

### Service Functions

- `generate_audio(text, output_path, voice_id, api_key)`: Converts text to speech using ElevenLabs API
- `generate_image(prompt, generator, model, save_path)`: Generates a face image using the specified AI image generator
- `generate_talking_head(audio_path, output_path, api_key, image_url)`: Generates a talking head video using RunwayML API

## Usage Example

```python
from app.tools.talking_head.service import generate_audio, generate_image, generate_talking_head

# Generate audio from text
text = "Hello, welcome to our product demonstration."
audio_path = "/tmp/speech.mp3"
voice_id = "your_elevenlabs_voice_id"
elevenlabs_api_key = "your_elevenlabs_api_key"
generate_audio(text, audio_path, voice_id, elevenlabs_api_key)

# Generate a custom face image (optional)
image_prompt = "A professional business person with a friendly smile"
image_path = "/tmp/face.jpg"

# Using DALL-E 3
image_url = generate_image(image_prompt, generator="dalle", model="dall-e-3", save_path=image_path)

# Or using Gemini Flash 2.0
# image_url = generate_image(image_prompt, generator="gemini", model="gemini-2.0-flash", save_path=image_path)

# Generate talking head video from audio and image
video_path = "/tmp/talking_head.mp4"
runwayml_api_key = "your_runwayml_api_key"
generate_talking_head(audio_path, video_path, runwayml_api_key, image_url)
```

## Troubleshooting

### Common Issues

- **ElevenLabs API Error**: Check that your API key is valid and that you have sufficient credits in your account
- **RunwayML API Error**: Ensure your API key is correct and that you're using a supported audio format
- **Video Generation Timeout**: For longer texts, the video generation process may take some time. Consider breaking up very long texts into smaller segments

### Error Messages

- `ElevenLabs API error: 401`: Invalid API key or authentication issue
- `ElevenLabs API error: 429`: Rate limit exceeded or insufficient credits
- `RunwayML API error: 400 - {"error":"Invalid API Version"}`: The RunwayML API version may have changed, check for updates
