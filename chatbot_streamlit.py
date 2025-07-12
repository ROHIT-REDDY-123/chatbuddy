import streamlit as st
import nltk
import string
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources (only the first time)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Preprocessing setup
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)

# Intents and responses
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

# Vectorization setup
intent_labels = []
all_patterns = []

for intent, data in intents.items():
    for pattern in data["patterns"]:
        all_patterns.append(preprocess(pattern))
        intent_labels.append(intent)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(all_patterns)

def get_intent(user_input):
    cleaned = preprocess(user_input)
    user_vec = vectorizer.transform([cleaned])
    similarity = cosine_similarity(user_vec, X)
    best_idx = similarity.argmax()
    confidence = similarity[0][best_idx]

    if confidence < 0.3:
        return "unknown"
    return intent_labels[best_idx]

def chatbot_response(user_input):
    intent = get_intent(user_input)
    return random.choice(intents[intent]["responses"])

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="ChatBuddy", page_icon="🤖")

st.title("🤖 ChatBuddy")
st.markdown("Ask me anything like greetings, my name, or say 'bye' to exit.")

# Store chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input form
with st.form(key="chat_form"):
    user_input = st.text_input("You:", "")
    submit = st.form_submit_button("Send")

# Display and process input
if submit and user_input.strip() != "":
    response = chatbot_response(user_input)
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("ChatBuddy", response))

# Show conversation history
for sender, msg in st.session_state.messages:
    st.markdown(f"**{sender}:** {msg}")
