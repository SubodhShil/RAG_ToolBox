import streamlit as st
import sounddevice as sd
import soundfile as sf
import numpy as np
from io import BytesIO
import time

def speaking_assistant_ai_page():

    st.title("Speaking Assistant AI")

    if 'recordings' not in st.session_state:
        st.session_state.recordings = []


if __name__ == "__main__":
    speaking_assistant_ai_page()