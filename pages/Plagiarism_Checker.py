import streamlit as st
import requests
import json
import re

def plagiarism_checker_page():
    st.title("Plagiarism Checker")
    st.write("Check your content for plagiarism with our AI-powered tool.")
    
    # File upload or text input section
    st.header("Enter Content to Check")
    
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
    
    # Initialize session state for LLM selection if not already done
    if 'selected_llm' not in st.session_state:
        st.session_state.selected_llm = 'gemini'
    
    # Add a checkbox for AI rephrasing option
    rephrase_option = st.checkbox("Rephrase flagged parts using AI", value=False)
    
    if st.button("Check for Plagiarism"):
        if 'text_to_check' in locals() and text_to_check:
            with st.spinner("Analyzing text for potential plagiarism..."):
                # Call the plagiarism checking API
                result = check_plagiarism(text_to_check, st.session_state.selected_llm)
                
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    # Display the results
                    display_plagiarism_results(result, text_to_check, rephrase_option)
        else:
            st.warning("Please enter some text or upload a file to check for plagiarism.")

def check_plagiarism(text, llm="gemini"):
    """Send text to the plagiarism checking API"""
    try:
        response = requests.post(
            f"https://langchain-grammar-check-api.onrender.com/plagiarism/{llm}/check_plagiarism",
            json={"text": text}
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def rephrase_text(text, llm="gemini"):
    """Send text to the paraphrasing API to rephrase it"""
    try:
        response = requests.post(
            f"https://langchain-grammar-check-api.onrender.com/paraphraser/{llm}/paraphrase",
            json={"text": text, "style": "Academic"}
        )
        return response.json().get("paraphrased_text", text)
    except Exception as e:
        st.warning(f"Could not rephrase text: {str(e)}")
        return text

def display_plagiarism_results(result, original_text, rephrase_option):
    """Display the plagiarism check results in a user-friendly way"""
    # Display the plagiarism score
    score = result.get("plagiarism_score", 0)
    
    # Create a color gradient based on the score
    if score < 15:
        score_color = "green"
        risk_level = "Low Risk"
    elif score < 40:
        score_color = "orange"
        risk_level = "Medium Risk"
    else:
        score_color = "red"
        risk_level = "High Risk"
    
    # Display the score with a gauge-like visualization
    st.markdown(f"### Plagiarism Score: <span style='color:{score_color}; font-size: 1.5em;'>{score}%</span> ({risk_level})", unsafe_allow_html=True)
    
    # Create a progress bar to visualize the score
    st.progress(score/100)
    
    # Display feedback
    st.subheader("Analysis Feedback")
    st.info(result.get("feedback", "No feedback available."))
    
    # Display flagged sentences
    flagged_sentences = result.get("flagged_sentences", [])
    if flagged_sentences:
        st.subheader("Potentially Plagiarized or AI-Generated Content")
        
        # Create a dictionary to store original and rephrased versions
        rephrased_versions = {}
        
        # If rephrasing is enabled, generate rephrased versions of flagged sentences
        if rephrase_option and flagged_sentences:
            with st.spinner("Generating AI-rephrased alternatives..."):
                for sentence in flagged_sentences:
                    rephrased_versions[sentence] = rephrase_text(sentence, st.session_state.selected_llm)
        
        # Display each flagged sentence with highlighting
        for i, sentence in enumerate(flagged_sentences):
            with st.expander(f"Flagged Text {i+1}"):
                st.markdown(f"**Original:** <span style='background-color: rgba(255, 165, 0, 0.3);'>{sentence}</span>", unsafe_allow_html=True)
                
                # Add a small explanation about why this might be flagged
                if "In conclusion" in sentence or "On the one hand" in sentence or "In summary" in sentence:
                    st.caption("⚠️ Contains common AI transition phrases")
                if len(sentence.split()) > 25:
                    st.caption("⚠️ Unusually long and complex sentence structure")
                if all(len(word) < 4 for word in sentence.split()[:5]):
                    st.caption("⚠️ Contains generic phrasing")
                
                if rephrase_option and sentence in rephrased_versions:
                    st.markdown(f"**AI-Rephrased Alternative:** <span style='background-color: rgba(144, 238, 144, 0.3);'>{rephrased_versions[sentence]}</span>", unsafe_allow_html=True)
        
        # If rephrasing is enabled, offer to download the rephrased version
        if rephrase_option and rephrased_versions:
            # Create a full rephrased version of the text
            rephrased_full_text = original_text
            for original, rephrased in rephrased_versions.items():
                rephrased_full_text = rephrased_full_text.replace(original, rephrased)
            
            st.download_button(
                label="Download Rephrased Version",
                data=rephrased_full_text,
                file_name="rephrased_text.txt",
                mime="text/plain"
            )
    else:
        st.success("No potentially plagiarized content was detected.")
    
    # Add tips section
    with st.expander("Tips to Avoid Plagiarism"):
        st.markdown("""
        ### Tips to Avoid Plagiarism:
        - Always cite your sources using proper citation formats (APA, MLA, Chicago, etc.)
        - Use quotation marks for direct quotes and provide proper attribution
        - Paraphrase information in your own words while still citing the original source
        - Combine information from multiple sources and add your own analysis
        - Use plagiarism checking tools before submitting your work
        - Keep detailed notes of all sources used during research
        - When in doubt, cite the source
        """)
    
    # Add a section about AI detection
    with st.expander("How to Avoid AI Detection"):
        st.markdown("""
        ### How to Make Your Writing Less AI-Detectable:
        - Add personal anecdotes and experiences that are unique to you
        - Vary your sentence structure and length
        - Avoid overused transition phrases like "In conclusion" or "On the one hand"
        - Include occasional minor grammatical errors or informal language
        - Use contractions (don't, can't, won't) which are more common in human writing
        - Add your unique perspective and critical thinking
        - Reference specific, less common sources or examples
        - Include humor, emotion, or personal opinions where appropriate
        """)

if __name__ == "__main__":
    plagiarism_checker_page()