import streamlit as st
import requests
import json
import time

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize session state for LLM selection if not already done
if 'selected_llm' not in st.session_state:
    st.session_state.selected_llm = 'gemini'

# Initialize session state for message processing
if 'processing_done' not in st.session_state:
    st.session_state.processing_done = True

# Page styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,100..900;1,100..900&family=Karla:ital,wght@0,200..800;1,200..800&family=Raleway:ital,wght@0,100..900;1,100..900&family=Sofia+Sans:ital,wght@0,1..1000;1,1..1000&display=swap');

html, body, [class*="css"] {
    font-family: "Raleway", sans-serif;
    font-family: "Karla", sans-serif;
    font-family: "Archivo", sans-serif;
    font-family: "Sofia Sans", sans-serif;
    color: #333333;
}

.stApp {
    font-family: "Raleway", sans-serif;
    font-family: "Karla", sans-serif;
    font-family: "Archivo", sans-serif;
    font-family: "Sofia Sans", sans-serif;
    background-color: #f8f9fa;
}

h1, h2, h3, h4, h5, h6 {
    font-family: "Raleway", sans-serif !important;
    font-family: "Karla", sans-serif !important;
    font-family: "Archivo", sans-serif !important;
    font-family: "Sofia Sans", sans-serif !important;
    color: #1e3a8a;
}

.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.chat-message.user {
    background-color: #f0f2f6;
    border-left: 5px solid #7c7c7c;
}

.chat-message.assistant {
    background-color: #e6f7ff;
    border-left: 5px solid #2b6cb0;
}

.chat-message .avatar {
    width: 20%;
}

.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
}

.chat-message .message {
    width: 80%;
    padding: 0 1.5rem;
    color: #333333;
}

</style>
""", unsafe_allow_html=True)

# Page title
st.title("AI Chat")
st.write("Chat with our AI assistant powered by state-of-the-art language models")

# Function to call the chat API
def chat_with_ai(message, model="gemini"):
    try:
        # API endpoint
        url = f"https://langchain-grammar-check-api.onrender.com/chat/{model}/chat"
        
        # Prepare the request payload
        payload = {
            "message": message,
            "conversation_history": []
        }
        
        # Make the API request
        response = requests.post(url, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

# Display chat messages
for message in st.session_state.chat_history:
    with st.container():
        if message["role"] == "user":
            st.markdown(f"<div class='chat-message user'><div class='message'>🧑‍💻 <b>You:</b> {message['content']}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-message assistant'><div class='message'>🤖 <b>AI:</b> {message['content']}</div></div>", unsafe_allow_html=True)

# Chat input
user_input = st.text_input("Type your message here...", key="user_message")

# When the user submits a message
if st.button("Send", key="send_button"):
    if user_input and st.session_state.processing_done:  # Only process if there's input and not already processing
        st.session_state.processing_done = False  # Set processing flag
        
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get AI response
        with st.spinner("AI is thinking..."):
            ai_response = chat_with_ai(user_input, st.session_state.selected_llm)
        
        # Add AI response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        
        # Reset processing flag
        st.session_state.processing_done = True
        
        # Force a rerun to update the UI
        st.rerun()

# Add a button to clear the chat history
if st.button("Clear Chat", key="clear_button"):
    st.session_state.chat_history = []
    st.rerun()

# Display current model information
st.sidebar.write(f"Current model: {st.session_state.selected_llm.capitalize()}")

# Footer
footer = """
<div style="
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    color: #888;
    padding: 10px;
    text-align: right;
    font-size: 14px;
    z-index: 999;
">
    AI Chat | Created with ⚡ by Subodh Chandra Shil
</div>
"""
st.markdown(footer, unsafe_allow_html=True)