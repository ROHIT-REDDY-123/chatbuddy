# Step 0: Install required packages (if you haven't already; run these in your terminal or Colab cell)
# !pip install nltk

import string
import random
import nltk
from difflib import get_close_matches

# Download NLTK resources (you only need to run this once)
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Initialize global NLP objects
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    """
    Perform basic NLP preprocessing:
      - Lowercasing
      - Tokenization
      - Removing punctuation
      - Removing stopwords
      - Lemmatization
    Returns the cleaned text as a list of lemmas.
    """
    # Lowercase the text
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    filtered_tokens = [w for w in tokens if w not in stop_words]
    
    # Lemmatize tokens
    lemmas = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    return lemmas

# Define response patterns and corresponding responses.
# Note: The keys here are example phrases (not preprocessed) that we expect to match.
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

def get_intent(user_input):
    """
    Determine the intent of the user input by preprocessing the text and then using fuzzy matching
    against our defined patterns. Returns the key from responses_dict if a match is found.
    """
    # Preprocess the user input into tokens (lemmas)
    input_tokens = preprocess(user_input)
    # Reconstruct a cleaned string from the tokens
    cleaned_input = " ".join(input_tokens)
    
    # For each intent, check if any of the pattern phrases (preprocessed as well) 
    # have a decent fuzzy match with the input.
    for intent, data in responses_dict.items():
        for pattern in data["patterns"]:
            # Preprocess the pattern for consistency
            pattern_tokens = preprocess(pattern)
            cleaned_pattern = " ".join(pattern_tokens)
            
            # Use get_close_matches: if input is close to pattern (similarity ratio > 0.7), we say it's a match.
            matches = get_close_matches(cleaned_input, [cleaned_pattern], n=1, cutoff=0.7)
            if matches:
                return intent
    return None

def chatbot_response(user_input):
    # First try to get the intent using fuzzy matching on preprocessed text
    intent = get_intent(user_input)
    
    if intent:
        # Retrieve a random response for the matched intent
        return random.choice(responses_dict[intent]["responses"])
    else:
        # Fallback if no intent is recognized
        return "Sorry, I didn't understand that. Can you rephrase?"

def main():
    print("🤖 ChatBuddy: Hello! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "exit", "goodbye"]:
            print("🤖 ChatBuddy: Goodbye! 👋")
            break
        response = chatbot_response(user_input)
        print("🤖 ChatBuddy:", response)

if __name__ == "__main__":
    main()

