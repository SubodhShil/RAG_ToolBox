
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

.input-container {
    position: fixed;
    width: 50%;
    left: 25%;
    bottom: 50px; /* pushes input just above footer */
    background-color: #262730;
    border: 1px solid #FF4B4B;
    border-radius: 10px;
    padding: 10px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 9999;
}

.input-text {
    width: 85%;
    padding: 10px;
    border: none;
    background-color: #262730;
    color: white;
    font-size: 16px;
}

.input-button {
    background-color: transparent;
    border: none;
    color: #FF4B4B;
    font-size: 24px;
    cursor: pointer;
}

.input-button:hover {
    color: #ff7777;
}

</style>
""", unsafe_allow_html=True)

def create_qa_interface():
    st.title("Multi-Modal AI Question Answering")
    # Actual input logic using Streamlit widgets
    # Create a bottom fixed input bar with a submit button to the right
    with st.container():
        col1, col2 = st.columns([8, 1])
        with col1:
            user_input = st.text_input(
                "",
                placeholder="Ask a question about ...",
                key="chat_input",
                label_visibility="collapsed"
            )
        with col2:
            submit = st.button("➤")


    # Display response (simulate thinking for now)
    if submit and user_input:
        st.write(f"**You asked:** {user_input}")
        with st.spinner("Thinking..."):
            # Simulate response
            st.success("Here's a sample answer based on the document.")


footer = """
<style>

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    color: #888;
    padding: 10px;
    text-align: right;
    font-size: 14px;
    z-index: 999;
}

</style>

<div class="footer">
    Multi-Modal Chat | Created with ⚡ by Subodh Chandra Shil
</div>
"""
st.markdown(footer, unsafe_allow_html=True)


if __name__ == "__main__":
    create_qa_interface()
