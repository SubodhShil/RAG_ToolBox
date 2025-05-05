import streamlit as st
import requests
import json

st.title("Grammar Check")
st.write("Improve your writing with our AI-powered grammar checker")

user_text = st.text_area("Enter your text here:", height=150)

def check_grammar(text, llm="gemini"):
    try:
        response = requests.post(
            f"https://langchain-grammar-check-api.onrender.com/{llm}/check_grammar",
            json={"text": text}
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


if st.button("Find Grammatical Mistakes"):
    if user_text:
        with st.spinner("Checking grammar..."):

            # Initialize session state for LLM selection
            if 'selected_llm' not in st.session_state:
                st.session_state.selected_llm = 'gemini'

            fixed_grammar = check_grammar(user_text, st.session_state.selected_llm)

            if "error" in fixed_grammar:
                st.error(f"Error: {fixed_grammar['error']}")
            else:
                st.subheader("Results:")

                # Original vs Corrected Text
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Original Text")
                    st.info(fixed_grammar["original_text"])
                
                with col2:
                    st.markdown("### Corrected Text")
                    st.success(fixed_grammar["corrected_text"])
                
                # Display corrections
                if fixed_grammar["corrections"]:
                    st.markdown("### Corrections")
                    
                    for i, correction in enumerate(fixed_grammar["corrections"]):
                        with st.expander(f"Correction {i+1}: {correction['type'].title()}"):
                            cols = st.columns([1, 1])
                            with cols[0]:
                                st.markdown("**Error:**")
                                st.markdown(f"<span style='color:red'>{correction['error']}</span>", unsafe_allow_html=True)
                            
                            with cols[1]:
                                st.markdown("**Suggestion:**")
                                st.markdown(f"<span style='color:green'>{correction['suggestion']}</span>", unsafe_allow_html=True)
                            
                            st.markdown("**Explanation:**")
                            st.markdown(f"_{correction['explanation']}_")
                            
                    # Summary
                    st.success(f"Found {len(fixed_grammar['corrections'])} grammar issues to fix.")
                else:
                    st.success("No grammar issues found. Your text looks good!")
                
                # Add a download button for the corrected text
                st.download_button(
                    label="Download Corrected Text",
                    data=fixed_grammar["corrected_text"],
                    file_name="corrected_text.txt",
                    mime="text/plain"
                )
    else:
        st.warning("Please enter some text to check.")
