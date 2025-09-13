# String Classification API

A FastAPI-based service that classifies input strings into four categories: emergency, translation, question, and general.

## Features

- **Emergency Detection**: Identifies urgent or emergency-related content
- **Translation Requests**: Detects translation needs and foreign language content
- **Question Classification**: Recognizes questions and queries
- **General Text**: Default category for other content

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST `/classify`

Classifies a string into one of four categories.

**Request Body:**

```json
{
  "text": "Your input string here"
}
```

**Response:**

```json
{
  "input_text": "Your input string here",
  "classification": "emergency|translation|question|general",
  "confidence": 0.85,
  "reasoning": "Explanation of why this classification was chosen"
}
```

### GET `/`

Returns basic API information and available endpoints.

### GET `/health`

Health check endpoint.

### GET `/docs`

Interactive API documentation (Swagger UI).

## Example Usage

### Using curl

```bash
# Emergency detection
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "Help! There is a fire emergency!"}'

# Translation request
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "How do you say hello in Spanish?"}'

# Question
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "What is the weather like today?"}'

# General text
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "I had a great day at the park."}'
```

### Using Python requests

```python
import requests

url = "http://localhost:8000/classify"

# Test different types of strings
test_strings = [
    "Emergency! Call 911 immediately!",
    "Translate this to French please",
    "What time is it?",
    "The weather is nice today"
]

for text in test_strings:
    response = requests.post(url, json={"text": text})
    result = response.json()
    print(f"Text: {text}")
    print(f"Classification: {result['classification']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Reasoning: {result['reasoning']}")
    print("-" * 50)
```

### Using JavaScript/fetch

```javascript
async function classifyText(text) {
  const response = await fetch("http://localhost:8000/classify", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: text }),
  });

  const result = await response.json();
  console.log(result);
}

// Example usage
classifyText("Help! Medical emergency!");
```

## Classification Categories

### Emergency

Detects text containing:

- Emergency keywords: emergency, urgent, help, fire, police, ambulance, etc.
- Crisis indicators: danger, critical, severe, injury
- Emergency numbers: 911, SOS

**Example texts:**

- "Emergency! Call 911!"
- "Urgent help needed - fire!"
- "Medical emergency in progress"

### Translation

Detects text containing:

- Translation requests: "translate", "what does X mean", "how do you say"
- Language indicators: español, français, deutsch, etc.
- Non-English characters (significant amount)

**Example texts:**

- "Translate this to Spanish"
- "What does 'bonjour' mean in English?"
- "こんにちは" (Japanese text)

### Question

Detects text containing:

- Question words: what, how, when, where, why, who, which
- Question patterns: can, could, would, should, is, are, do, does
- Ending with question mark

**Example texts:**

- "What is the weather like?"
- "How do I get to the airport?"
- "Can you help me?"

### General

Default category for text that doesn't match the above patterns.

**Example texts:**

- "I love programming"
- "The movie was great"
- "Today is a beautiful day"

## Configuration

The classification logic uses keyword matching and pattern recognition. You can modify the keywords and patterns in the `classify_string()` function in `app.py` to customize the classification behavior.

## Development

To run in development mode with auto-reload:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Testing

You can test the API using the interactive documentation at `http://localhost:8000/docs` after starting the server.

## Response Format

All classification responses include:

- `input_text`: The original input string
- `classification`: One of four categories (emergency, translation, question, general)
- `confidence`: A score between 0 and 1 indicating classification confidence
- `reasoning`: Human-readable explanation of why this classification was chosen

## Error Handling

The API handles common errors:

- Empty or whitespace-only input returns HTTP 400
- Server errors return HTTP 500 with error details
- Invalid JSON returns HTTP 422

## License

This project is open source and available under the MIT License.
