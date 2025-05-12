import streamlit as st
import requests
import io
from PIL import Image
import pytesseract
from pytesseract import TesseractNotFoundError
import cv2
import numpy as np

# Set page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Image to Text Converter",
    page_icon="📷",
    layout="wide"
)

# Now you can add the title and other elements
st.title("Image To Text")
st.write("Generate text from your image!")

# Sidebar for options
with st.sidebar:
    st.header("Options")
    ocr_engine = st.selectbox(
        "OCR Engine",
        ["Tesseract", "Google Cloud Vision (API Key Required)"]
    )
    
    language = st.selectbox(
        "Language",
        ["English", "Spanish", "French", "German", "Chinese", "Japanese"]
    )
    
    lang_code = {
        "English": "eng",
        "Spanish": "spa",
        "French": "fra",
        "German": "deu",
        "Chinese": "chi_sim",
        "Japanese": "jpn"
    }

# Function to perform OCR with Tesseract
def perform_ocr_tesseract(image, lang="eng"):
    try:
        text = pytesseract.image_to_string(image, lang=lang)
        return text
    except TesseractNotFoundError:
        return "Error: Tesseract is not installed or not in PATH. Please install Tesseract OCR first."
    except Exception as e:
        return f"Error: {str(e)}"

# Function to perform OCR with Google Cloud Vision
def perform_ocr_google_vision(image):
    # This would require Google Cloud Vision API setup
    # Placeholder for actual implementation
    api_key = st.secrets.get("GOOGLE_VISION_API_KEY", None)
    if not api_key:
        return "Error: Google Cloud Vision API key not found. Please add it to your Streamlit secrets."
    
    # Convert image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # This is a placeholder for the actual API call
    return "Google Cloud Vision API integration would go here."

# Function to process image and extract text
def process_image(image, engine="Tesseract", lang="eng"):
    if engine == "Tesseract":
        return perform_ocr_tesseract(image, lang)
    else:
        return perform_ocr_google_vision(image)

# Main content area
st.header("Upload an Image")

# Create tabs for different input methods
tab1, tab2, tab3 = st.tabs(["Upload Image", "Image URL", "Camera Input"])

with tab1:
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Process button
        if st.button("Extract Text from Uploaded Image"):
            with st.spinner("Extracting text..."):
                text = process_image(image, ocr_engine, lang_code[language])
                
                # Display results
                st.subheader("Extracted Text:")
                st.text_area("", text, height=250)
                
                # Download button for extracted text
                st.download_button(
                    label="Download Text",
                    data=text,
                    file_name="extracted_text.txt",
                    mime="text/plain"
                )

with tab2:
    url = st.text_input("Enter Image URL")
    
    if url:
        try:
            # Fetch image from URL
            response = requests.get(url)
            image = Image.open(io.BytesIO(response.content))
            
            # Display the image
            st.image(image, caption="Image from URL", use_column_width=True)
            
            # Process button
            if st.button("Extract Text from URL Image"):
                with st.spinner("Extracting text..."):
                    text = process_image(image, ocr_engine, lang_code[language])
                    
                    # Display results
                    st.subheader("Extracted Text:")
                    st.text_area("", text, height=250)
                    
                    # Download button for extracted text
                    st.download_button(
                        label="Download Text",
                        data=text,
                        file_name="extracted_text.txt",
                        mime="text/plain"
                    )
        except Exception as e:
            st.error(f"Error loading image from URL: {str(e)}")

with tab3:
    st.write("Take a picture with your camera")
    
    # Camera input is supported in Streamlit
    camera_image = st.camera_input("Take a picture")
    
    if camera_image is not None:
        # Display the captured image
        image = Image.open(camera_image)
        
        # Process button
        if st.button("Extract Text from Camera Image"):
            with st.spinner("Extracting text..."):
                text = process_image(image, ocr_engine, lang_code[language])
                
                # Display results
                st.subheader("Extracted Text:")
                st.text_area("", text, height=250)
                
                # Download button for extracted text
                st.download_button(
                    label="Download Text",
                    data=text,
                    file_name="extracted_text.txt",
                    mime="text/plain"
                )


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
    Image to Text Converter | Created with ⚡ by Subodh Chandra Shil
</div>
"""
st.markdown(footer, unsafe_allow_html=True)