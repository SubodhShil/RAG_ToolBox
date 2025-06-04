import streamlit as st
import requests
import json

st.title("Text Paraphraser")
st.write("Transform your text with our AI-powered paraphrasing tool")

user_text = st.text_area("Enter your text here:", height=150)

# Style selection
style = st.selectbox(
    "Select paraphrasing style:",
    ["Fluency", "Humanize", "Formal", "Academic", "Simple", "Creative", "Shorten"],
    index=0
)

# Style descriptions
style_descriptions = {
    "Fluency": "Makes the text flow naturally and smoothly, focusing on readability.",
    "Humanize": "Makes the text sound more conversational, warm, and relatable.",
    "Formal": "Uses professional language, avoids contractions, and maintains a respectful tone.",
    "Academic": "Uses scholarly language, precise terminology, and complex sentence structures.",
    "Simple": "Uses straightforward language, short sentences, and common words.",
    "Creative": "Uses vivid language, metaphors, and unique expressions.",
    "Shorten": "Condenses the text while preserving the key information."
}

# Display the description of the selected style
st.info(style_descriptions[style])

def paraphrase_text(text, style, llm="gemini"):
    try:
        response = requests.post(
            f"https://langchain-grammar-check-api.onrender.com/paraphraser/{llm}/paraphrase",
            json={"text": text, "style": style}
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


if st.button("Paraphrase Text"):
    if user_text:
        with st.spinner(f"Paraphrasing in {style} style..."):
            # Initialize session state for LLM selection if not already done
            if 'selected_llm' not in st.session_state:
                st.session_state.selected_llm = 'gemini'

            paraphrased = paraphrase_text(user_text, style, st.session_state.selected_llm)

            if "error" in paraphrased:
                st.error(f"Error: {paraphrased['error']}")
            else:
                st.subheader("Results:")

                # Original vs Paraphrased Text
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Original Text")
                    st.info(paraphrased["original_text"])
                
                with col2:
                    st.markdown(f"### Paraphrased Text ({style})")
                    st.success(paraphrased["paraphrased_text"])
                
                # Add a download button for the paraphrased text
                st.download_button(
                    label="Download Paraphrased Text",
                    data=paraphrased["paraphrased_text"],
                    file_name="paraphrased_text.txt",
                    mime="text/plain"
                )
    else:
        st.warning("Please enter some text to paraphrase.")

# Add tips section
with st.expander("Tips for Better Results"):
    st.markdown("""
    ### Tips for Better Results:
    - Provide clear, well-structured text for the best paraphrasing results
    - For longer texts, consider breaking them into paragraphs
    - Different styles work better for different types of content
    - Academic style works well for research papers and formal documents
    - Humanize style is great for customer communications
    - Creative style works best for marketing and storytelling
    - Shorten style is ideal for summarizing lengthy content
    """)

# Add a footer
st.markdown("""
---
*Powered by Gemini AI*
""")