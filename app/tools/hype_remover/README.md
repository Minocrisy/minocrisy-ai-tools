# Hype Remover Tool

The Hype Remover tool removes exaggerated claims and marketing hype from text using OpenAI's language models or xAI's Grok model.

## Features

- Transform marketing copy into factual content
- Adjust the strength of hype removal (mild, moderate, strong)
- Add custom hype terms to target specific marketing language
- Provide context about the text to improve accuracy
- Toggle between OpenAI and xAI (Grok) models
- Get detailed explanations of changes made to the text

## How It Works

1. The user enters text containing marketing hype or exaggerated claims
2. The user can adjust settings like strength, custom hype terms, and context
3. The text is processed by either OpenAI's GPT models or xAI's Grok model
4. The tool returns:
   - The processed text with hype removed
   - A list of changes made with explanations
   - An overall hype score for the original text
   - An accuracy score for the processed text

## API Requirements

- **OpenAI API**: Used for language processing with GPT models
  - Required environment variables:
    - `OPENAI_API_KEY`: Your OpenAI API key

- **xAI API** (optional): Used for language processing with Grok models
  - Required environment variables:
    - `XAI_API_KEY`: Your xAI API key
    - `XAI_API_URL`: The xAI API endpoint (https://api.x.ai/v1)

## Implementation Details

### Routes

- `GET /tools/hype-remover/`: Renders the Hype Remover tool interface
- `POST /tools/hype-remover/process`: Processes text to remove hype
- `POST /tools/hype-remover/feedback`: Stores user feedback on hype removal results

### Service Functions

- `remove_hype(text, strength, custom_hype_terms, context, api_key, use_xai)`: Removes hype from text using the specified model
- `store_feedback(original_text, processed_text, user_rating, user_comments)`: Stores user feedback for model improvement

## Usage Example

```python
from app.tools.hype_remover.service import remove_hype

# Process text with OpenAI
result = remove_hype(
    text="Our revolutionary product is the ultimate solution that will transform your life!",
    strength="moderate",
    custom_hype_terms=["revolutionary", "ultimate"],
    context="Product marketing for a software tool",
    api_key="your_openai_api_key",
    use_xai=False
)

# Process text with xAI (Grok)
result = remove_hype(
    text="Our revolutionary product is the ultimate solution that will transform your life!",
    strength="strong",
    custom_hype_terms=["revolutionary", "ultimate"],
    context="Product marketing for a software tool",
    use_xai=True
)

# Print the processed text
print(result["processed_text"])
# Example output: "Our product is a solution that can help improve your workflow."

# Print the changes made
for change in result["changes"]:
    print(f"Original: {change['original']}")
    print(f"Replacement: {change['replacement']}")
    print(f"Reason: {change['reason']}")
    print(f"Confidence: {change['confidence']}")
```

## Strength Levels

- **Mild**: Maintains the overall message but replaces clearly exaggerated claims with more measured, factual statements. Only modifies phrases that contain obvious hype or exaggeration.
- **Moderate** (default): Replaces promotional language and exaggerated statements with more measured, factual alternatives. Focuses on modifying claims that lack substantiation or use excessive superlatives.
- **Strong**: Aggressively identifies and removes marketing hype, exaggerations, and unsubstantiated claims. Replaces all promotional language, superlatives, and exaggerated claims with strictly factual, neutral statements.

## Troubleshooting

### Common Issues

- **OpenAI API Error**: Check that your API key is valid and that you have sufficient credits in your account
- **xAI API Error**: Ensure your API key is correct and that you're using the correct API endpoint
- **Model Availability**: If using xAI, ensure you're using an available model (e.g., grok-2-1212 instead of grok-3)
- **Response Format Error**: Some OpenAI models don't support the JSON response format. The tool automatically handles this, but you may need to use a different model if you encounter errors.

### Error Messages

- `OpenAI API error: 401`: Invalid API key or authentication issue
- `OpenAI API error: 429`: Rate limit exceeded or insufficient credits
- `OpenAI API error: 400 - Invalid parameter: 'response_format'`: The model doesn't support JSON response format
- `xAI API error: 404 - The model does not exist`: The specified model is not available or doesn't exist
