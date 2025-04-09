
import streamlit as st
import openai
from PIL import Image
import io

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,100..900;1,100..900&family=Karla:ital,wght@0,200..800;1,200..800&family=Raleway:ital,wght@0,100..900;1,100..900&family=Sofia+Sans:ital,wght@0,1..1000;1,1..1000&display=swap');

html, body, [class*="css"] {
    font-family: "Raleway", sans-serif;
    font-family: "Karla", sans-serif;
    font-family: "Archivo", sans-serif;
    font-family: "Sofia Sans", sans-serif;
}

.stApp {
    font-family: "Raleway", sans-serif;
    font-family: "Karla", sans-serif;
    font-family: "Archivo", sans-serif;
    font-family: "Sofia Sans", sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: "Raleway", sans-serif !important;
    font-family: "Karla", sans-serif !important;
    font-family: "Archivo", sans-serif !important;
    font-family: "Sofia Sans", sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

def create_qa_interface():
    st.title("Multi-Modal AI Question Answering")

    # Configure page layout
    st.markdown("""
    <style>
    .chat-container {
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    .user-message {
        background-color: #e6f3ff;
        text-align: right;
    }
    .assistant-message {
        background-color: #f0f0f0;
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True)


    if 'messages' not in st.session_state:
        st.session_state.messages = []


    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        with st.container():
            st.markdown(f"""
            <div class="chat-container {'user-message' if role == 'user' else 'assistant-message'}">
                <b>{role.title()}:</b> {content}
            </div>
            """, unsafe_allow_html=True)

    # User input
    user_question = st.text_input("Ask your question here:", key="user_input")

    # Optional file upload
    uploaded_file = st.file_uploader(
        "Upload an image (optional)", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # Send button
    if st.button("Send"):
        if user_question:
            # Add user message to chat history
            st.session_state.messages.append(
                {"role": "user", "content": user_question})

            # Here you would typically make an API call to your backend or AI model
            # For demonstration, we'll just echo the question
            response = f"This is a sample response to: {user_question}"

            # Add assistant response to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": response})

            # Clear the input
            st.session_state.user_input = ""

            # Rerun to update the chat display
            st.experimental_rerun()

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()


if __name__ == "__main__":
    create_qa_interface()
