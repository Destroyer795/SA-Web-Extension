# Sentiment Analyzer Web Extension

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-API-yellow)](https://huggingface.co/spaces/destroyer795/Sentiment-Analyzer-Extension)

A powerful Chrome extension that uses AI to instantly analyze the emotional tone of any text on the web. Powered by a fine-tuned DistilBERT model, it detects positive, negative, or neutral/mixed sentiments with confidence scoring.

## Features

- **Instant Analysis**: Right-click any selected text and analyze its sentiment in seconds
- **AI-Powered**: Uses a fine-tuned DistilBERT model optimized for sentiment classification
- **Confidence Scoring**: Displays confidence levels with visual progress bars
- **Clean UI**: Modern, animated interface with color-coded sentiment indicators
- **Privacy-Focused**: Text is only processed when you explicitly request it
- **Fast Response**: Optimized API hosted on Hugging Face Spaces

## How It Works

1. **Select** any text on a webpage
2. **Right-click** and choose "Analyze Sentiment"
3. **View** instant results with sentiment classification and confidence score

## Tech Stack

### Extension (Frontend)
- Chrome Manifest V3
- Vanilla JavaScript
- CSS3 with smooth animations
- Chrome Extension APIs

### Backend API
- **Framework**: Flask
- **Model**: Fine-tuned DistilBERT (3-class sentiment classifier)
- **ML Library**: Transformers (Hugging Face)
- **Deployment**: Hugging Face Spaces
- **Server**: Gunicorn

## Installation

### Installing the Extension

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Destroyer795/SA-Web-Extension.git
   cd SA-Web-Extension
   ```

2. **Load in Chrome**:
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable **Developer mode** (toggle in top-right)
   - Click **Load unpacked**
   - Select the `extension` folder from this project

3. **Start using**:
   - Select any text on a webpage
   - Right-click and choose "Analyze Sentiment"

### Running the API Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask server**:
   ```bash
   python app.py
   ```

3. **Update API endpoint** (if running locally):
   - Open `extension/popup.js`
   - Change `API_URL` to `http://localhost:7860/predict`

## Configuration

### Model Details
- **Model Type**: DistilBERT for Sequence Classification
- **Classes**: Positive, Negative, Neutral
- **Confidence Threshold**: 70% (scores below are marked as "Neutral / Mixed")
- **Location**: `./sentiment_analyzer_pro/`

### API Endpoints

#### `POST /predict`
Analyzes sentiment of provided text.

**Request**:
```json
{
  "text": "This is an amazing product!"
}
```

**Response**:
```json
{
  "sentiment": "Positive",
  "score": 0.9542,
  "confidence_flag": "High"
}
```

#### `GET /`
Health check endpoint.

## Project Structure

```
.
├── extension/              # Chrome extension files
│   ├── manifest.json      # Extension configuration
│   ├── popup.html         # Popup UI
│   ├── popup.js           # Popup logic
│   ├── popup.css          # Popup styles
│   └── background.js      # Background service worker
├── sentiment_analyzer_pro/ # Fine-tuned DistilBERT model
│   ├── model.safetensors
│   ├── config.json
│   ├── tokenizer.json
│   └── ...
├── app.py                 # Flask API server
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
└── README.md
```

## Sentiment Classification Logic

The model returns a label and confidence score:

- **High Confidence** (≥70%): Returns the predicted sentiment (Positive/Negative)
- **Low Confidence** (<70%): Returns "Neutral / Mixed" to handle ambiguous or sarcastic text

This approach reduces false positives for edge cases like sarcasm or mixed emotions.

## Deployment

### Hugging Face Spaces

The API is currently deployed at:
```
https://destroyer795-sentiment-analyzer-extension.hf.space/
```

To deploy your own:
1. Create a [Hugging Face Space](https://huggingface.co/spaces)
2. Upload the project files
3. Update the `API_URL` in `extension/popup.js`

### Docker

Build and run using Docker:
```bash
docker build -t sentiment-analyzer .
docker run -p 7860:7860 sentiment-analyzer
```

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Hugging Face** for the Transformers library and hosting platform
- **DistilBERT** model architecture by Hugging Face
- Chrome Extension APIs documentation

## Contact

- **Developer**: [Destroyer795](https://github.com/Destroyer795)
- **Hugging Face Space**: [Sentiment-Analyzer-Extension](https://huggingface.co/spaces/destroyer795/Sentiment-Analyzer-Extension)

---

Made with love using AI and Flask
