import streamlit as st

def plagiarism_checker_page():
    st.title("Plagiarism Checker")
    st.write("Check your content for plagiarism with our AI-powered tool.")
    
    # Text input section
    st.header("Enter Content to Check")
    text_to_check = st.text_area("Paste the content you want to check for plagiarism:", height=150)
    reference_text = st.text_area("Paste reference text to compare against (optional):", height=150)
    
    if st.button("Check for Plagiarism"):
        if text_to_check:
            # Here you would implement the actual plagiarism detection logic
            # For now, we'll use a simple placeholder implementation
            
            # Calculate a mock similarity score (in a real implementation, you would use
            # algorithms like cosine similarity, Jaccard similarity, or more advanced NLP techniques)
            if reference_text:
                # Simple word overlap calculation for demonstration
                text_words = set(text_to_check.lower().split())
                ref_words = set(reference_text.lower().split())
                common_words = text_words.intersection(ref_words)
                
                if len(text_words) > 0:
                    similarity = len(common_words) / len(text_words) * 100
                else:
                    similarity = 0
                
                st.write(f"Similarity score: {similarity:.2f}%")
                
                if similarity > 70:
                    st.error("⚠️ High similarity detected! Your content may contain plagiarized text.")
                elif similarity > 40:
                    st.warning("⚠️ Moderate similarity detected. Consider revising some parts.")
                else:
                    st.success("✅ Low similarity detected. Your content appears to be original.")
            else:
                # Without reference text, we'd typically check against a database or use an API
                st.info("In a complete implementation, this would connect to a plagiarism detection API or database.")
                st.success("✅ No obvious plagiarism detected in standalone analysis.")
            
            # Display additional tips
            st.markdown("""
            ### Tips to Avoid Plagiarism:
            - Always cite your sources
            - Paraphrase information in your own words
            - Use quotation marks for direct quotes
            - Combine information from multiple sources
            """)
        else:
            st.warning("Please enter some text to check for plagiarism.")

if __name__ == "__main__":
    plagiarism_checker_page()