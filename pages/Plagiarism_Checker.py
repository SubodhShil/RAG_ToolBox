import streamlit as st
import requests
import json
import re


def plagiarism_checker_page():
    st.title("Plagiarism Checker")
    st.write("Check your content for plagiarism with our AI-powered tool.")
    
    # Add tabs for text input and file upload
    tab1, tab2 = st.tabs(["Text Input", "File Upload"])
    
    with tab1:
        text_to_check = st.text_area("Paste the content you want to check for plagiarism:", height=200)
    
    with tab2:
        uploaded_file = st.file_uploader("Upload a .txt or .docx file", type=["txt", "docx"])
        if uploaded_file is not None:
            # Handle different file types
            if uploaded_file.name.endswith('.txt'):
                text_to_check = uploaded_file.read().decode("utf-8")
                st.success(f"File '{uploaded_file.name}' loaded successfully!")
            elif uploaded_file.name.endswith('.docx'):
                try:
                    import docx
                    doc = docx.Document(uploaded_file)
                    text_to_check = "\n".join([para.text for para in doc.paragraphs])
                    st.success(f"File '{uploaded_file.name}' loaded successfully!")
                except Exception as e:
                    st.error(f"Error reading .docx file: {str(e)}")
                    st.info("Please make sure you have the python-docx package installed.")
                    text_to_check = ""
    
    if st.button("Check for Plagiarism"):
        if 'text_to_check' in locals() and text_to_check:
            with st.spinner("Analyzing text for potential plagiarism..."):
                # Call the plagiarism checking API
                result = check_plagiarism(text_to_check)
                
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    # Display the results
                    display_plagiarism_results(result, text_to_check)
        else:
            st.warning("Please enter some text or upload a file to check for plagiarism.")

def check_plagiarism(text):
    """Send text to the plagiarism checking API"""
    try:
        response = requests.post(
            "https://bdstall-duplicate-content-checking-api.onrender.com/api/v1/ai/moderation/content-duplication-check",
            json={"user_description_input": text}
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def display_plagiarism_results(result, original_text):
    """Display the plagiarism check results in a user-friendly way"""
    is_duplicate = result.get("is_duplicate", False)
    message = result.get("message", "")
    url = result.get("url", "")

    if is_duplicate:
        st.error(f"Plagiarism Detected: {message}")
        if url:
            st.markdown(f"Source: [{url}]({url})")
    else:
        st.success("No plagiarism detected.")

if __name__ == "__main__":
    plagiarism_checker_page()