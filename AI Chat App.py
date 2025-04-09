import streamlit as st
import pandas as pd
import numpy as np

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


# Application Title
st.write("# RAG ToolBox")

# Define the gradient_div function first
def gradient_div(content, bg, page_link):
    features_section = f"""
        <a href="{page_link}" target="_self" style="
            height: 70px;
            width: 100%;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 25px;
            display: flex;
            text-align: center;
            flex-direction: column;
            color: white;
            font-size: 18px;
            font-weight: 600;
            background: {bg};
            align-items: center;
            justify-content: center;
            box-shadow: 0px 8px 16px rgba(0,0,0,0.1);
            text-decoration: none;
            transition: all 0.3s ease;
        ">
            {content}
        </a>
        <style> 
            a:hover {{
                transform: translateY(-3px);
                box-shadow: 0px 12px 24px rgba(0,0,0,0.15);
            }}
        </style>
    """
    return features_section

# Animated instruction box
st.markdown("""
<div style="
    padding: 20px;
    margin: 20px 0;
    border-radius: 12px;
    background: rgba(30, 30, 40, 0.7);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(100, 149, 237, 0.3);
    text-align: center;
">
    <div style="
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, 
            rgba(30, 30, 40, 0) 0%, 
            rgba(100, 149, 237, 0.3) 50%, 
            rgba(30, 30, 40, 0) 100%);
        animation: shimmer 3s infinite;
        z-index: 0;
    "></div>
    <div style="
        position: relative;
        z-index: 1;
        color: #f0f0f0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
    ">
        <h3 style="color: #64b5f6; margin-top: 0; width: 100%; text-align: center;">📚 Welcome to RAG ToolBox! 🎉</h3>
        <p style="margin-bottom: 16px; width: 100%; text-align: center;"> Explore our AI-powered tools below</p>
    </div>
</div>

<style>
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    #emoji::after {
        content: '💡';
        animation: changeEmoji 4s infinite;
    }
    
    @keyframes changeEmoji {
        0% { content: '💡'; }
        20% { content: '✨'; }
        40% { content: '🚀'; }
        60% { content: '🎯'; }
        80% { content: '🔮'; }
        100% { content: '💡'; }
    }
    
    a:hover {
        transform: translateY(-3px);
        box-shadow: 0px 12px 24px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Create a 2-column layout
col1, col2 = st.columns(2)

# Place boxes in columns
with col1:
    st.markdown(
        gradient_div(
            "Generate AI Arts",
            "linear-gradient(to right, #FF416C, #FF4B2B)",
            "/AI_Art"
        ),
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        gradient_div(
            "Grammar Check",
            "linear-gradient(to right, #4776E6, #8E54E9)",
            "/Grammar_Check"
        ),
        unsafe_allow_html=True
    )

# Second row
with col1:
    st.markdown(
        gradient_div(
            "Image to Text",
            "linear-gradient(to right, #11998e, #38ef7d)",
            "/Image_To_Text"
        ),
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        gradient_div(
            "Multi-Modal AI Chat",
            "linear-gradient(to right, #2980B9, #6DD5FA)",
            "/Multi_Modal_AI"
        ),
        unsafe_allow_html=True
    )

# Third row with Resume Maker and Voice Changer
with col1:
    st.markdown(
        gradient_div(
            "Resume Maker",
            "linear-gradient(to right, #8E2DE2, #4A00E0)",
            "/Resume_Maker"
        ),
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        gradient_div(
            "Voice Changer",
            "linear-gradient(to right, #FF5F6D, #FFC371)",
            "/Voice_AI"
        ),
        unsafe_allow_html=True
    )

# Sidebar
api_method = st.sidebar.selectbox(
    '### API Methods',
    ('Freemium', 'Your Own API')
)


if api_method == 'Freemium':
    model = st.sidebar.selectbox(
        'Select Model',
        ('Gemini', 'Mistral', 'DeepSeek')
    )
    st.sidebar.write(f"Selected model: {model}")

else:
    api_input = st.sidebar.text_input(
        "Enter your API key", key="api_input", type="password")
