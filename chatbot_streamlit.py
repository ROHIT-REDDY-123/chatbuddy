# import streamlit as st

# def chatbot_response(user_input):
#     user_input = user_input.lower()

#     if "hello" in user_input or "hi" in user_input:
#         return "Hello! How can I help you today?"
#     elif "how are you" in user_input:
#         return "I'm just a bot, but I'm doing great! How about you?"
#     elif "your name" in user_input:
#         return "I'm ChatBuddy, your simple chatbot!"
#     elif "bye" in user_input or "exit" in user_input:
#         return "Goodbye! Have a nice day!"
#     elif "help" in user_input:
#         return "You can ask me about greetings, my name, or say bye to exit."
#     else:
#         return "Sorry, I didn't understand that. Can you rephrase?"

# st.title("🤖 ChatBuddy – Simple Rule-Based Chatbot")
# user_input = st.text_input("You:", "")

# if user_input:
#     response = chatbot_response(user_input)
#     st.text_area("ChatBuddy:", value=response, height=100)

import streamlit as st
import string
import random
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Optional: Add a title and intro
st.set_page_config(page_title="ChatBuddy 🤖", page_icon="💬")
st.title("🤖 ChatBuddy – Rule-Based NLP Chatbot")
st.markdown("Ask me about greetings, my name, or say 'bye' to exit.")

# -------------------
# 1. Preprocessing
# -------------------
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = re.findall(r'\b\w+\b', text)
    return " ".join(tokens)

# -------------------
# 2. Intents
# -------------------
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

# -------------------
# 3. Build training data
# -------------------
all_patterns = []
intent_labels = []

for intent, data in intents.items():
    for pattern in data["patterns"]:
        all_patterns.append(preprocess(pattern))
        intent_labels.append(intent)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(all_patterns)

# -------------------
# 4. Intent Prediction
# -------------------
def get_intent(user_input):
    cleaned = preprocess(user_input)
    user_vec = vectorizer.transform([cleaned])
    similarity = cosine_similarity(user_vec, X)
    best_idx = similarity.argmax()
    confidence = similarity[0][best_idx]

    if confidence < 0.3:
        return "unknown"
    return intent_labels[best_idx]

# -------------------
# 5. Generate response
# -------------------
def chatbot_response(user_input):
    intent = get_intent(user_input)
    return random.choice(intents[intent]["responses"])

# -------------------
# 6. Streamlit UI
# -------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", "")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip() != "":
    response = chatbot_response(user_input)
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("ChatBuddy", response))

# Show conversation
for sender, msg in st.session_state.messages:
    st.markdown(f"**{sender}:** {msg}")
