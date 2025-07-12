import streamlit as st

def chatbot_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?"
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! How about you?"
    elif "your name" in user_input:
        return "I'm ChatBuddy, your simple chatbot!"
    elif "bye" in user_input or "exit" in user_input:
        return "Goodbye! Have a nice day!"
    elif "help" in user_input:
        return "You can ask me about greetings, my name, or say bye to exit."
    else:
        return "Sorry, I didn't understand that. Can you rephrase?"

st.title("🤖 ChatBuddy – Simple Rule-Based Chatbot")
user_input = st.text_input("You:", "")

if user_input:
    response = chatbot_response(user_input)
    st.text_area("ChatBuddy:", value=response, height=100)

