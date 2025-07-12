import streamlit as st
from app import chatbot_response

st.set_page_config(page_title="ChatBuddy", page_icon="🤖")
st.title("🤖 ChatBuddy - Rule-Based Chatbot")
st.markdown("Type a message to start chatting with ChatBuddy!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", "")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    response = chatbot_response(user_input)
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("ChatBuddy", response))

# Show chat history
for sender, message in st.session_state.messages:
    st.markdown(f"**{sender}:** {message}")
