# app.py

import re
import random
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required resources (only needed in first run)
nltk.download('stopwords')
nltk.download('wordnet')

# Preprocessing setup
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = re.findall(r'\b\w+\b', text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)

# Intent database
intents = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "good morning", "good evening"],
        "responses": ["Hi! How can I help you?", "Hello! What can I do for you?"]
    },
    "bye": {
        "patterns": ["bye", "goodbye", "exit", "see you"],
        "responses": ["Goodbye!", "See you later!", "Take care!"]
    },
    "name": {
        "patterns": ["your name", "who are you", "what is your name"],
        "responses": ["I'm ChatBuddy, your friendly chatbot!"]
    },
    "thanks": {
        "patterns": ["thanks", "thank you", "thx"],
        "responses": ["You're welcome!", "Anytime!", "Glad to help!"]
    },
    "unknown": {
        "patterns": [],
        "responses": ["Sorry, I didn't understand that. Can you rephrase?"]
    }
}

# Build training data for TF-IDF
intent_labels = []
all_patterns = []

for intent, data in intents.items():
    for pattern in data["patterns"]:
        all_patterns.append(preprocess(pattern))
        intent_labels.append(intent)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(all_patterns)

def get_intent(user_input):
    cleaned_input = preprocess(user_input)
    input_vec = vectorizer.transform([cleaned_input])
    similarities = cosine_similarity(input_vec, X)
    max_index = similarities.argmax()
    confidence = similarities[0][max_index]
    return intent_labels[max_index] if confidence >= 0.3 else "unknown"

def chatbot_response(user_input):
    intent = get_intent(user_input)
    return random.choice(intents[intent]["responses"])
