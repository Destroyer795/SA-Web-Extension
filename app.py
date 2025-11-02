from flask import Flask, request, jsonify
import torch
import torch.nn as nn
from gensim.models import KeyedVectors
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
from nltk.corpus import stopwords as nltk_stopwords
from spellchecker import SpellChecker

class RNN(nn.Module):
    def __init__(self, input_dim, embedding_dim, hidden_dim, output_dim, n_layers, bidirectional, dropout, embedding_weights):
        super().__init__()
        self.embedding = nn.Embedding.from_pretrained(embedding_weights, padding_idx=0)
        self.rnn = nn.LSTM(embedding_dim, hidden_dim, num_layers=n_layers, bidirectional=bidirectional, dropout=dropout)
        self.fc = nn.Linear(hidden_dim * 2, output_dim)
        self.dropout = nn.Dropout(dropout)
    def forward(self, text, text_lengths):
        embedded = self.embedding(text)
        packed_embedded = nn.utils.rnn.pack_padded_sequence(embedded, text_lengths.to('cpu'))
        packed_output, (hidden, cell) = self.rnn(packed_embedded)
        hidden = self.dropout(torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1))
        return self.fc(hidden)


stop_words = set(nltk_stopwords.words('english'))
negation_words = {
    'not', 'no', 'nor', 'never', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't",
    'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
    'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", "can't"
}
stop_words = stop_words - negation_words
lemmatizer = WordNetLemmatizer()
spell = SpellChecker()

def preprocess_text(text):
    text = re.sub(r"it's", "it is", text)
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"we're", "we are", text)
    text = re.sub(r"they're", "they are", text)
    text = re.sub(r"you're", "you are", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"n't", " not", text)
    
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    
    return lemmatized_tokens

print("Loading models...")
device = torch.device('cpu')
word_vectors = KeyedVectors.load('word_vectors.kv')
embedding_weights = torch.FloatTensor(word_vectors.vectors)
INPUT_DIM, EMBEDDING_DIM = embedding_weights.shape
HIDDEN_DIM, OUTPUT_DIM, N_LAYERS, DROPOUT = 256, 1, 2, 0.5
BIDIRECTIONAL = True
model = RNN(INPUT_DIM, EMBEDDING_DIM, HIDDEN_DIM, OUTPUT_DIM, N_LAYERS, BIDIRECTIONAL, DROPOUT, embedding_weights)
model.load_state_dict(torch.load('sentiment_model.pth', map_location=device))
model.to(device)
model.eval()
print("Models loaded successfully!")

app = Flask(__name__)

def predict_sentiment(sentence):
    model.eval()
    preprocessed_tokens = preprocess_text(sentence)
    if preprocessed_tokens:
        misspelled = spell.unknown(preprocessed_tokens)
        final_tokens = [(spell.correction(word) or word) if word in misspelled else word for word in preprocessed_tokens]
    else:
        final_tokens = []

    if not final_tokens: return 0.5
    indexed = [word_vectors.key_to_index.get(t, -1) for t in final_tokens]
    indexed = [i for i in indexed if i != -1]
    if not indexed: return 0.5

    length = torch.LongTensor([len(indexed)])
    tensor = torch.LongTensor(indexed).to(device).unsqueeze(1)
    prediction = torch.sigmoid(model(tensor, length))
    
    return prediction.item()

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    sentence = data['text']
    score = predict_sentiment(sentence)

    words_in_sentence = set(re.findall(r"[\w']+", sentence.lower()))
    if any(word in negation_words for word in words_in_sentence):
        if score > 0.5:
            score = 1.0 - score

    sentiment = 'Positive' if score > 0.6 else 'Negative' if score < 0.4 else 'Neutral'
    
    return jsonify({'sentiment': sentiment, 'score': score})

if __name__ == '__main__':
    print("\nRunning Local Tests:")
    
    test_sentence_1 = "its not good"
    score_1 = predict_sentiment(test_sentence_1)
    if any(word in negation_words for word in set(re.findall(r"[\w']+", test_sentence_1.lower()))):
        if score_1 > 0.5: score_1 = 1.0 - score_1
    print(f"Sentence: '{test_sentence_1}' | Final Score: {score_1:.4f} | Sentiment: {'Positive' if score_1 > 0.6 else 'Negative' if score_1 < 0.4 else 'Neutral'}")

    test_sentence_2 = "This movie was absolutely amazing"
    score_2 = predict_sentiment(test_sentence_2)
    if any(word in negation_words for word in set(re.findall(r"[\w']+", test_sentence_2.lower()))):
        if score_2 > 0.5: score_2 = 1.0 - score_2
    print(f"Sentence: '{test_sentence_2}' | Final Score: {score_2:.4f} | Sentiment: {'Positive' if score_2 > 0.6 else 'Negative' if score_2 < 0.4 else 'Neutral'}")

    test_sentence_3 = "The service can't be described as fast"
    score_3 = predict_sentiment(test_sentence_3)
    if any(word in negation_words for word in set(re.findall(r"[\w']+", test_sentence_3.lower()))):
        if score_3 > 0.5: score_3 = 1.0 - score_3
    print(f"Sentence: '{test_sentence_3}' | Final Score: {score_3:.4f} | Sentiment: {'Positive' if score_3 > 0.6 else 'Negative' if score_3 < 0.4 else 'Neutral'}")
    
    print("\nTo start the web server, run 'flask run' in the terminal.")