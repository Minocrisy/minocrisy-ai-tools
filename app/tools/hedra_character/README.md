# Hedra Character Video Tool

The Hedra Character Video tool generates character videos with synchronized speech using Hedra's API. It allows users to create videos of characters speaking their text with customizable character models and voices.

## Features

- Create videos of characters speaking your text
- Choose from various character models
- Select different voices for customization
- Generate engaging character videos quickly

## How It Works

1. The user enters text that they want the character to speak
2. The user selects a character model and voice
3. The text and selections are sent to the Hedra API
4. The API generates a video of the selected character speaking the text with the chosen voice
5. The resulting video is saved and presented to the user for viewing or download

## API Requirements

- **Hedra API**: Used for character video generation
  - Required environment variables:
    - `HEDRA_API_KEY`: Your Hedra API key
    - `HEDRA_API_URL`: The Hedra API endpoint (https://api.hedra.com/v1)

## Implementation Details

### Routes

- `GET /tools/hedra-character/`: Renders the Hedra Character Video tool interface
- `POST /tools/hedra-character/generate`: Processes text input and generates a character video
- `GET /tools/hedra-character/characters`: Gets a list of available character models
- `GET /tools/hedra-character/voices`: Gets a list of available voices

### Service Functions

- `generate_character_video(text, character_id, voice_id, output_path)`: Generates a character video using Hedra API
- `list_characters()`: Gets a list of available character models from Hedra API
- `list_voices()`: Gets a list of available voices from Hedra API

## Usage Example

```python
from app.utils.hedra_api import generate_character_video, list_characters, list_voices

# List available characters
characters = list_characters()
for character in characters:
    print(f"ID: {character['id']}, Name: {character['name']}")

# List available voices
voices = list_voices()
for voice in voices:
    print(f"ID: {voice['id']}, Name: {voice['name']}, Gender: {voice['gender']}")

# Generate a character video
text = "Hello, I'm a virtual character created using the Hedra API."
character_id = "character_123"  # Use an ID from list_characters()
voice_id = "voice_456"  # Use an ID from list_voices()
output_path = "/path/to/output/video.mp4"

video_path = generate_character_video(
    text=text,
    character_id=character_id,
    voice_id=voice_id,
    output_path=output_path
)

print(f"Video generated at: {video_path}")
```

## Troubleshooting

### Common Issues

- **Hedra API Error**: Check that your API key is valid and that you have sufficient credits in your account
- **Character or Voice Not Found**: Ensure you're using valid character and voice IDs
- **Video Generation Timeout**: For longer texts, the video generation process may take some time

### Error Messages

- `Hedra API error: 401`: Invalid API key or authentication issue
- `Hedra API error: 404`: Resource not found (character or voice ID may be invalid)
- `Error generating video: Failed to generate video with Hedra API`: General error during video generation
