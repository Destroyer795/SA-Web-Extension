"""
Sentiment Analyzer Pro API
--------------------------
A Flask-based API that serves a fine-tuned DistilBERT model for sentiment analysis.
It provides endpoints for health checks and sentiment prediction, with logic to handle
low-confidence predictions as "Neutral / Mixed".
"""

from flask import Flask, request, jsonify
from transformers import pipeline
import torch

app = Flask(__name__)

# Configuration
# Path to the local model directory. Ensure this matches the unzipped folder structure.
MODEL_PATH = "./sentiment_analyzer_pro"

# Initialize the model pipeline
# device=-1 forces CPU usage, which is compatible with standard hosting environments.
print("Loading DistilBERT 3-class model...")
try:
    classifier = pipeline(
        "sentiment-analysis", 
        model=MODEL_PATH, 
        tokenizer=MODEL_PATH,
        device=-1 
    )
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    """
    Analyze the sentiment of the provided text.
    
    Expected JSON Input:
        {"text": "Text to analyze"}
        
    Returns:
        JSON response containing the sentiment label, confidence score, and a confidence flag.
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    sentence = data['text']
    
    # Perform inference
    # The classifier returns a list of dicts, e.g., [{'label': 'POSITIVE', 'score': 0.98}]
    result = classifier(sentence)[0]
    
    label = result['label']
    score = result['score']
    
    # Logic for handling low confidence predictions
    # A threshold of 0.70 is used to identify ambiguous or sarcastic text.
    if score < 0.70:
        final_sentiment = "Neutral / Mixed"
        confidence_flag = "Low"
    else:
        final_sentiment = label.capitalize()
        confidence_flag = "High"
    
    return jsonify({
        'sentiment': final_sentiment, 
        'score': round(score, 4),
        'confidence_flag': confidence_flag
    })

@app.route('/', methods=['GET'])
def health_check():
    """Simple health check endpoint to verify the API is running."""
    return "Sentiment Analyzer Pro API is online."

if __name__ == '__main__':
    # Runing     the Flask app
    # Host '0.0.0.0' exposes the server to external connections.
    # Port 7860 is the default for many cloud platforms (e.g., Hugging Face Spaces).
    app.run(host='0.0.0.0', port=7860)