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
from chatbot import chatbot_response  # ✅ This will work if app.py exists

st.title("🤖 ChatBuddy – Rule-Based Bot")

if "chat" not in st.session_state:
    st.session_state.chat = []

with st.form("chat_form"):
    user_input = st.text_input("You:")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    response = chatbot_response(user_input)
    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("Bot", response))

for sender, msg in st.session_state.chat:
    st.markdown(f"**{sender}:** {msg}")
