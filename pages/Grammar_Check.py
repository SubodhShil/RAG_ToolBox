import streamlit as st

st.title("Grammar Check")

user_text = st.text_area("Enter your text here:", height=150)

if st.button("Find Grammatical Mistakes"):

    st.subheader("Results:")

    if user_text:
        st.write(user_text)
    else:
        st.warning("Please enter some text to check.")
