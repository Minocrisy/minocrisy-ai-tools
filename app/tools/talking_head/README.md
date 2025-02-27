# Talking Head Tool

The Talking Head tool generates animated talking head videos from text input using ElevenLabs for text-to-speech and RunwayML for animation.

## Features

- Convert text to natural-sounding speech using ElevenLabs API
- Animate a virtual presenter with lip-syncing using RunwayML API
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

## Implementation Details

### Routes

- `GET /tools/talking-head/`: Renders the Talking Head tool interface
- `POST /tools/talking-head/generate`: Processes text input and generates a talking head video

### Service Functions

- `generate_audio(text, output_path, voice_id, api_key)`: Converts text to speech using ElevenLabs API
- `generate_talking_head(audio_path, output_path, api_key)`: Generates a talking head video using RunwayML API

## Usage Example

```python
from app.tools.talking_head.service import generate_audio, generate_talking_head

# Generate audio from text
text = "Hello, welcome to our product demonstration."
audio_path = "/tmp/speech.mp3"
voice_id = "your_elevenlabs_voice_id"
elevenlabs_api_key = "your_elevenlabs_api_key"
generate_audio(text, audio_path, voice_id, elevenlabs_api_key)

# Generate talking head video from audio
video_path = "/tmp/talking_head.mp4"
runwayml_api_key = "your_runwayml_api_key"
generate_talking_head(audio_path, video_path, runwayml_api_key)
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
