# Grok Chat Tool

The Grok Chat tool provides an interface for chatting with xAI's Grok model for intelligent conversations and assistance. It supports both text-based conversations and visual analysis with Grok Vision.

## Features

- Chat with xAI's Grok model for intelligent conversations
- Upload images for visual analysis with Grok Vision
- Upload documents (PDF, DOCX, TXT) for content analysis
- Adjust temperature for more focused or creative responses
- Choose between different Grok models (Grok-2, Grok-2 Vision)
- Maintain conversation history for context-aware responses

## How It Works

1. The user enters a message and optionally uploads an image or document
2. If an image is uploaded, the tool automatically selects the Grok Vision model
3. The message and file (if any) are sent to the xAI API
4. Grok processes the input and generates a response
5. The conversation history is maintained for context-aware follow-up responses

## API Requirements

- **xAI API**: Used for accessing Grok models
  - Required environment variables:
    - `XAI_API_KEY`: Your xAI API key
    - `XAI_API_URL`: The xAI API endpoint (https://api.x.ai/v1)

## Implementation Details

### Routes

- `GET /tools/xai-chat/`: Renders the Grok Chat tool interface
- `POST /tools/xai-chat/chat`: Processes chat messages and file uploads
- `POST /tools/xai-chat/clear`: Clears conversation history

### Available Models

- `grok-2-1212`: Standard Grok-2 model for text-based conversations
- `grok-2-vision-1212`: Grok-2 Vision model for image and document analysis

### File Upload Support

The tool supports uploading the following file types:
- Images (JPG, PNG, GIF)
- Documents (PDF, DOCX, TXT)

When an image is uploaded:
1. The interface automatically switches to the Grok Vision model
2. The image is displayed in the chat interface
3. The image is processed along with the user's message

## Usage Example

```python
import requests
import json

# Text-only chat
response = requests.post(
    "http://localhost:8080/tools/xai-chat/chat",
    headers={"Content-Type": "application/json"},
    data=json.dumps({
        "message": "What is the capital of France?",
        "model": "grok-2-1212",
        "temperature": 0.7
    })
)
result = response.json()
print(result["response"])

# Chat with image upload
files = {
    "file": ("image.jpg", open("path/to/image.jpg", "rb"), "image/jpeg"),
    "message": (None, "What's in this image?"),
    "model": (None, "grok-2-vision-1212"),
    "temperature": (None, "0.7")
}
response = requests.post(
    "http://localhost:8080/tools/xai-chat/chat",
    files=files
)
result = response.json()
print(result["response"])
```

## Troubleshooting

### Common Issues

- **xAI API Error**: Ensure your API key is correct and that you're using the correct API endpoint
- **Model Availability**: Ensure you're using available models (e.g., grok-2-1212, grok-2-vision-1212)
- **File Size Limits**: Large files may cause upload issues or timeouts
- **File Format Support**: Ensure you're uploading supported file formats

### Error Messages

- `xAI API error: 401`: Invalid API key or authentication issue
- `xAI API error: 404 - The model does not exist`: The specified model is not available or doesn't exist
- `Error: File is required for vision model`: When using the vision model, a file must be uploaded
- `Error: No file selected`: A file upload was attempted but no file was selected
