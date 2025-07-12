# chatbot_streamlit.py

import streamlit as st
from app import chatbot_response

st.set_page_config(page_title="ChatBuddy", page_icon="🤖")
st.title("🤖 ChatBuddy")
st.markdown("Ask me anything like greetings, my name, or say 'bye' to exit.")

# Session-based message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", "")
    submitted = st.form_submit_button("Send")

# Process and respond
if submitted and user_input.strip() != "":
    response = chatbot_response(user_input)
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("ChatBuddy", response))

# Display chat history
for sender, msg in st.session_state.messages:
    st.markdown(f"**{sender}:** {msg}")

