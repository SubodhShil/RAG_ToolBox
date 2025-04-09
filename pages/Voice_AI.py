import streamlit as st
import sounddevice as sd
import soundfile as sf
import numpy as np
from io import BytesIO
import time

def voice_ai_page():
    st.title("Voice Changer AI")
    
    # Initialize session state for voice recordings
    if 'recordings' not in st.session_state:
        st.session_state.recordings = []
    
    # Voice input section
    st.header("Record Your Voice")
    duration = st.slider("Recording duration (seconds)", 1, 10, 3)
    
    if st.button("Start Recording"):
        st.write("Recording... Speak now!")
        fs = 44100  # Sample rate
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished
        st.session_state.current_recording = recording
        st.session_state.recordings.append(recording)
        st.success("Recording complete!")
    
    # Playback section
    if hasattr(st.session_state, 'current_recording'):
        st.header("Your Recordings")
        
        # Current recording
        st.subheader("Current Recording")
        audio_bytes = BytesIO()
        sf.write(audio_bytes, st.session_state.current_recording, 44100, format='WAV')
        st.audio(audio_bytes, format='audio/wav')
        
        # Previous recordings
        if len(st.session_state.recordings) > 1:
            st.subheader("Previous Recordings")
            for i, rec in enumerate(st.session_state.recordings[:-1]):
                audio_bytes = BytesIO()
                sf.write(audio_bytes, rec, 44100, format='WAV')
                st.audio(audio_bytes, format='audio/wav')

if __name__ == "__main__":
    voice_ai_page()