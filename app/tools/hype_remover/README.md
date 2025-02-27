# Hype Remover Tool

The Hype Remover tool removes exaggerated claims and marketing hype from text using OpenAI's language models, xAI's Grok model, or Google's Gemini Flash 2.0 model.

## Features

- Transform marketing copy into factual content
- Adjust the strength of hype removal (mild, moderate, strong)
- Add custom hype terms to target specific marketing language
- Provide context about the text to improve accuracy
- Toggle between OpenAI, xAI (Grok), and Google Gemini Flash 2.0 models
- Get detailed explanations of changes made to the text
- Research topics to get factual information
- Save and manage outputs with local memory
- Export content to different formats (X posts, Google Docs)

## How It Works

1. The user enters text containing marketing hype or exaggerated claims
2. The user can adjust settings like strength, custom hype terms, and context
3. The text is processed by OpenAI's GPT models, xAI's Grok model, or Google's Gemini Flash 2.0 model
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

- **Google Gemini API** (optional): Used for language processing with Gemini Flash 2.0
  - Required environment variables:
    - `GEMINI_API_KEY`: Your Google Gemini API key

## Implementation Details

### Routes

- `GET /tools/hype-remover/`: Renders the Hype Remover tool interface
- `POST /tools/hype-remover/process`: Processes text to remove hype
- `POST /tools/hype-remover/research`: Researches a topic and returns information
- `POST /tools/hype-remover/save`: Saves processed text to local memory
- `GET /tools/hype-remover/saved`: Gets all saved outputs for the current user
- `GET /tools/hype-remover/saved/<output_id>`: Gets a specific saved output
- `DELETE /tools/hype-remover/saved/<output_id>`: Deletes a specific saved output
- `POST /tools/hype-remover/export/x`: Formats text as an X (Twitter) post
- `POST /tools/hype-remover/export/google-doc`: Formats text as Google Doc content
- `POST /tools/hype-remover/feedback`: Stores user feedback on hype removal results

### Service Functions

- `remove_hype(text, strength, custom_hype_terms, context, api_key, use_xai, use_gemini)`: Removes hype from text using the specified model
- `research_topic(topic, api_key, use_xai, use_gemini)`: Researches a topic using the specified model
- `save_output(title, original_text, processed_text, source_url)`: Saves processed text to local memory
- `get_saved_outputs()`: Gets all saved outputs for the current user
- `get_saved_output(output_id)`: Gets a specific saved output
- `delete_saved_output(output_id)`: Deletes a specific saved output
- `create_x_post(text)`: Formats text as an X (Twitter) post
- `create_google_doc_content(title, text, source_url)`: Formats text as Google Doc content
- `store_feedback(original_text, processed_text, user_rating, user_comments)`: Stores user feedback for model improvement

## Usage Examples

### Hype Removal

```python
from app.tools.hype_remover.service import remove_hype

# Process text with OpenAI
result = remove_hype(
    text="Our revolutionary product is the ultimate solution that will transform your life!",
    strength="moderate",
    custom_hype_terms=["revolutionary", "ultimate"],
    context="Product marketing for a software tool",
    api_key="your_openai_api_key",
    use_xai=False,
    use_gemini=False
)

# Process text with xAI (Grok)
result = remove_hype(
    text="Our revolutionary product is the ultimate solution that will transform your life!",
    strength="strong",
    custom_hype_terms=["revolutionary", "ultimate"],
    context="Product marketing for a software tool",
    use_xai=True,
    use_gemini=False
)

# Process text with Google Gemini Flash 2.0
result = remove_hype(
    text="Our revolutionary product is the ultimate solution that will transform your life!",
    strength="moderate",
    custom_hype_terms=["revolutionary", "ultimate"],
    context="Product marketing for a software tool",
    use_xai=False,
    use_gemini=True
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

### Research

```python
from app.tools.hype_remover.service import research_topic

# Research a topic with Gemini Flash 2.0
result = research_topic(
    topic="Quantum Computing",
    use_xai=False,
    use_gemini=True
)

# Print the research summary
print(result["summary"])

# Print the key points
for point in result["key_points"]:
    print(f"- {point}")

# Print the sources
for source in result["sources"]:
    print(f"- {source['title']}")
    if source.get('url'):
        print(f"  URL: {source['url']}")
    if source.get('description'):
        print(f"  Description: {source['description']}")
```

### Saving and Retrieving Outputs

```python
from app.tools.hype_remover.service import save_output, get_saved_outputs, get_saved_output, delete_saved_output

# Save an output
output_id = save_output(
    title="Dehyped Marketing Copy",
    original_text="Our revolutionary product is the ultimate solution!",
    processed_text="Our product is a helpful solution.",
    source_url="https://example.com/marketing"
)

# Get all saved outputs
outputs = get_saved_outputs()
for id, output in outputs.items():
    print(f"ID: {id}")
    print(f"Title: {output['title']}")
    print(f"Timestamp: {output['timestamp']}")

# Get a specific saved output
output = get_saved_output(output_id)
if output:
    print(f"Title: {output['title']}")
    print(f"Original: {output['original_text']}")
    print(f"Processed: {output['processed_text']}")

# Delete a saved output
success = delete_saved_output(output_id)
```

### Export Formats

```python
from app.tools.hype_remover.service import create_x_post, create_google_doc_content

# Format as X (Twitter) post
x_post = create_x_post("Our product is a helpful solution that can improve your workflow.")
print(x_post)  # Will be truncated to 280 characters if necessary

# Format as Google Doc content
doc_content = create_google_doc_content(
    title="Dehyped Marketing Copy",
    text="Our product is a helpful solution that can improve your workflow.",
    source_url="https://example.com/marketing"
)
print(doc_content)
```

## Strength Levels

- **Mild**: Maintains the overall message but replaces clearly exaggerated claims with more measured, factual statements. Only modifies phrases that contain obvious hype or exaggeration.
- **Moderate** (default): Replaces promotional language and exaggerated statements with more measured, factual alternatives. Focuses on modifying claims that lack substantiation or use excessive superlatives.
- **Strong**: Aggressively identifies and removes marketing hype, exaggerations, and unsubstantiated claims. Replaces all promotional language, superlatives, and exaggerated claims with strictly factual, neutral statements.

## Troubleshooting

### Common Issues

- **OpenAI API Error**: Check that your API key is valid and that you have sufficient credits in your account
- **xAI API Error**: Ensure your API key is correct and that you're using the correct API endpoint
- **Gemini API Error**: Verify your API key is valid and that you have the necessary permissions
- **Model Availability**: If using xAI, ensure you're using an available model (e.g., grok-2-1212 instead of grok-3)
- **Response Format Error**: Some OpenAI models don't support the JSON response format. The tool automatically handles this, but you may need to use a different model if you encounter errors.

### Error Messages

- `OpenAI API error: 401`: Invalid API key or authentication issue
- `OpenAI API error: 429`: Rate limit exceeded or insufficient credits
- `OpenAI API error: 400 - Invalid parameter: 'response_format'`: The model doesn't support JSON response format
- `xAI API error: 404 - The model does not exist`: The specified model is not available or doesn't exist
- `Gemini API error: 400`: Invalid request format or parameters
- `Gemini API error: 401`: Invalid API key or authentication issue
- `Gemini API error: 429`: Rate limit exceeded or quota reached
