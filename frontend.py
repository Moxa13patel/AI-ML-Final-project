import streamlit as st
import requests
import torch

# Set page config
st.set_page_config(page_title="Mental Health Chatbot", layout="wide")

# Store conversation history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Custom CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #f3e5f5, #e3f2fd);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100vh;
}
.chat-title {
    font-size: 36px;
    font-weight: 700;
    text-align: center;
    padding-top: 20px;
    margin-bottom: 10px;
    background: linear-gradient(to right, #ab47bc, #42a5f5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.chat-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    height: 3vh; /* Adjust this */
}
.chat-bubble-user {
    background-color: #c5cae9;
    color: #000;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 8px 0;
    align-self: flex-end;
    max-width: 70%;
}
.how{
    background-color: #fce4ec;
    color: #000;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 8px 0;
    align-self: flex-start;
    max-width: 70%;            
}
.chat-bubble-bot {
    background-color: #fce4ec;
    color: #000;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 8px 0;
    align-self: flex-start;
    max-width: 70%;
}
.input-row {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
    position: fixed;
    bottom: 100%; /* ⬅️ Adjust this to move input row up/down */
    left: 0;
    width: 100%;
    background: linear-gradient(to right, #42a5f5, #ec407a);
    border: black;
}
.send-btn-style {
    background: linear-gradient(to right, #42a5f5, #ec407a);
    color: white;
    border-radius: 50%;
    padding: 0.5em 0.75em;
    font-size: 20px;
    position: relative;
    top: -55px;
    left: 90%;
}
.input-container {
    margin-top: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    padding-bottom: 300px;  /* Reduced from larger value */
}
.stApp {
    background: linear-gradient(to right, #f3e5f5, #e3f2fd);
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='chat-title'>🧠 Mental Health Chatbot</div>", unsafe_allow_html=True)
st.markdown("<div class='how'>How are you feeling today?</div>", unsafe_allow_html=True)

# Display chat history
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for message in st.session_state.chat_history:
    role = message["role"]
    content = message["content"]
    bubble_class = "chat-bubble-user" if role == "user" else "chat-bubble-bot"
    st.markdown(f"<div class='{bubble_class}'>{content}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Clear input if just submitted
if st.session_state.get("clear_input"):
    st.session_state.temp_input = ""
    st.session_state.clear_input = False

# Input area
col1, col2 = st.columns([10, 1])

# Initialize chat_history_ids
if "chat_history_ids" not in st.session_state:
    st.session_state.chat_history_ids = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "temp_input" not in st.session_state:
    st.session_state.temp_input = ""

# Use temp_input to avoid modifying input widget directly
with col1:
    st.text_input(" ", label_visibility="collapsed", key="temp_input")

with col2:
    if st.button("➤", help="Send", key="send_btn"):
        user_input = st.session_state.temp_input
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            try:
                payload = {
                    "message": user_input,
                    "chat_history_ids": st.session_state.chat_history_ids.tolist() if st.session_state.chat_history_ids is not None else None
                }
                response = requests.post("http://127.0.0.1:5000/chat", json=payload)
                data = response.json()
                bot_reply = data.get("response", "Sorry, something went wrong.")
                updated_history = data.get("chat_history_ids")

                st.session_state.chat_history.append({"role": "bot", "content": bot_reply})
                if updated_history:
                    st.session_state.chat_history_ids = torch.tensor(updated_history)
            except Exception:
                st.session_state.chat_history.append({"role": "bot", "content": "⚠️ Failed to connect to backend."})

            st.session_state.clear_input = True  # Set flag
            st.rerun()


