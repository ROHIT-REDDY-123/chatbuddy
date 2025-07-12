# 📌 Install dependencies (run this in terminal if not done yet):
# pip install streamlit nltk

import streamlit as st
import nltk
import string
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from difflib import get_close_matches

# ✅ First-time setup for NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# ✨ NLP tools
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# 🔁 Preprocess function
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
    return " ".join(tokens)

# 🧠 Intent and responses dictionary
responses_dict = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "good morning", "good evening"],
        "responses": ["Hello! How can I help you today?", "Hi there! What can I do for you?"]
    },
    "how_are_you": {
        "patterns": ["how are you", "how are you doing", "how is it going"],
        "responses": ["I'm just a bot, but I'm doing great! How about you?"]
    },
    "bot_name": {
        "patterns": ["your name", "who are you", "what is your name"],
        "responses": ["I'm ChatBuddy, your upgraded chatbot with NLP!"]
    },
    "goodbye": {
        "patterns": ["bye", "goodbye", "see you", "exit"],
        "responses": ["Goodbye! Have a nice day!", "See you later!"]
    },
    "help": {
        "patterns": ["help", "assist me", "what can you do"],
        "responses": ["You can greet me, ask my name, or say bye to exit."]
    }
}

# 🎯 Match user input to intent
def get_intent(user_input):
    cleaned_input = preprocess(user_input)
    for intent, data in responses_dict.items():
        for pattern in data["patterns"]:
            cleaned_pattern = preprocess(pattern)
            if get_close_matches(cleaned_input, [cleaned_pattern], n=1, cutoff=0.7):
                return intent
    return None

# 💬 NLP-enhanced chatbot response
def chatbot_response(user_input):
    intent = get_intent(user_input)
    if intent:
        return random.choice(responses_dict[intent]["responses"])
    return "Sorry, I didn't understand that. Can you rephrase?"

# 🖼️ Streamlit App UI
st.title("🤖 ChatBuddy – NLP-Enhanced Chatbot (Streamlit)")

user_input = st.text_input("You:", "")

if user_input:
    response = chatbot_response(user_input)
    st.text_area("ChatBuddy:", value=response, height=100)
