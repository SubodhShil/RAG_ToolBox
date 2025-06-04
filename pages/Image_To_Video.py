import streamlit as st
import requests
import io
from PIL import Image
# Remove pytesseract import to fix the error
import cv2
import numpy as np

# Set page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Image to Video Converter",
    page_icon="🎬",
    layout="wide"
)

# Now you can add the title and other elements
st.title("Image To Video")
st.write("Convert your images into a video with AI-generated transitions!")

# Sidebar for options
with st.sidebar:
    st.header("Video Options")
    
    video_quality = st.select_slider(
        "Video Quality",
        options=["Low", "Medium", "High", "Ultra"],
        value="Medium"
    )
    
    transition_type = st.selectbox(
        "Transition Type",
        ["Fade", "Dissolve", "Wipe", "Zoom", "AI-Generated"]
    )
    
    video_duration = st.slider(
        "Video Duration (seconds)",
        min_value=5,
        max_value=60,
        value=15,
        step=5
    )

# Main content area
st.header("Upload Images")

# Create a container for the image upload and prompt
with st.container():
    # Multiple file uploader for images
    uploaded_files = st.file_uploader(
        "Choose multiple image files", 
        type=["jpg", "jpeg", "png", "bmp"],
        accept_multiple_files=True
    )
    
    # Prompt input for AI-generated content
    prompt = st.text_area(
        "Enter a prompt to guide the AI video generation",
        placeholder="Example: Create a smooth transition between these nature images with a dreamy atmosphere",
        height=100
    )
    
    # Display uploaded images in a grid
    if uploaded_files:
        st.subheader(f"Preview: {len(uploaded_files)} Images Uploaded")
        
        # Create a grid layout for the images
        cols = st.columns(min(4, len(uploaded_files)))
        
        for i, uploaded_file in enumerate(uploaded_files):
            with cols[i % min(4, len(uploaded_files))]:
                # Display the uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption=f"Image {i+1}", use_column_width=True)
        
        # Generate video button
        if st.button("Generate Video"):
            if prompt:
                with st.spinner("Generating your video with AI..."):
                    # Placeholder for actual video generation logic
                    st.info("In a complete implementation, this would connect to a video generation API.")
                    
                    # Display a success message
                    st.success("✅ Video generation request submitted!")
                    
                    # Placeholder for video preview
                    st.subheader("Video Preview")
                    st.write("Your video would appear here once generated.")
                    
                    # Placeholder for download button
                    st.download_button(
                        label="Download Video",
                        data=io.BytesIO(b"Placeholder for actual video data"),
                        file_name="ai_generated_video.mp4",
                        mime="video/mp4",
                        disabled=True
                    )
            else:
                st.warning("Please enter a prompt to guide the AI video generation.")
    else:
        st.info("Please upload at least two images to create a video.")

# Tips section
with st.expander("Tips for Better Results"):
    st.markdown("""
    ### Tips for Better Results:
    - Upload images with similar dimensions for the best transitions
    - Use 5-10 images for optimal video length
    - Be specific in your prompt about the style and mood you want
    - Higher quality settings will take longer to process
    - For best results, arrange your images in the desired sequence before uploading
    """)

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
    Image to Video Converter | Created with ⚡ by Subodh Chandra Shil
</div>
"""
st.markdown(footer, unsafe_allow_html=True)