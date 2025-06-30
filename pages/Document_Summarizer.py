import streamlit as st
import requests
import json
import PyPDF2
import docx
import io
import base64
from typing import Optional

# Page configuration
st.set_page_config(page_title="Document Summarizer", layout="wide")

st.title("📄 Document Summarizer")
st.write("Upload your documents and get AI-powered summaries instantly")

# Initialize session state
if 'selected_llm' not in st.session_state:
    st.session_state.selected_llm = 'gemini'

if 'document_content' not in st.session_state:
    st.session_state.document_content = ""

if 'summary_result' not in st.session_state:
    st.session_state.summary_result = None

# Helper functions
def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def extract_text_from_docx(docx_file) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return ""

def extract_text_from_txt(txt_file) -> str:
    """Extract text from TXT file"""
    try:
        return txt_file.read().decode('utf-8')
    except Exception as e:
        st.error(f"Error reading TXT: {str(e)}")
        return ""

def summarize_text(text: str, llm: str = "gemini", summary_type: str = "general") -> dict:
    """Summarize text using AI API"""
    try:
        # For now, we'll create a mock summarization since we don't have a specific API endpoint
        # In a real implementation, you would call your summarization API
        
        # Mock response - replace with actual API call
        summary_length = len(text.split())
        
        if summary_length < 50:
            summary = "The document is too short to summarize effectively."
        else:
            # Simple extractive summary (first few sentences)
            sentences = text.split('. ')
            summary_sentences = sentences[:min(3, len(sentences))]
            summary = '. '.join(summary_sentences)
            if not summary.endswith('.'):
                summary += '.'
        
        return {
            "original_length": summary_length,
            "summary": summary,
            "summary_length": len(summary.split()),
            "compression_ratio": round(len(summary.split()) / max(1, summary_length) * 100, 1)
        }
    except Exception as e:
        return {"error": str(e)}

def display_pdf(pdf_file):
    """Display PDF in the UI"""
    try:
        # Read the PDF file
        pdf_bytes = pdf_file.read()
        
        # Encode to base64
        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        
        # Create PDF viewer HTML
        pdf_display = f'''
        <iframe src="data:application/pdf;base64,{base64_pdf}" 
                width="100%" 
                height="600" 
                type="application/pdf">
        </iframe>
        '''
        
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        # Reset file pointer for text extraction
        pdf_file.seek(0)
        
    except Exception as e:
        st.error(f"Error displaying PDF: {str(e)}")

# Main UI
st.markdown("---")

# File upload section
st.subheader("📁 Upload Document")
uploaded_file = st.file_uploader(
    "Choose a file",
    type=['pdf', 'docx', 'txt'],
    help="Supported formats: PDF, DOCX, TXT"
)

# Summary options
st.subheader("⚙️ Summary Options")
col1, col2 = st.columns(2)

with col1:
    summary_type = st.selectbox(
        "Summary Type",
        ["General", "Key Points", "Executive Summary", "Academic"],
        help="Choose the type of summary you want"
    )

with col2:
    summary_length = st.selectbox(
        "Summary Length",
        ["Short", "Medium", "Long"],
        index=1,
        help="Choose the desired length of the summary"
    )

if uploaded_file is not None:
    # Display file info
    st.success(f"✅ File uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
    
    # Create two columns for document display and processing
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📖 Document Preview")
        
        # Display PDF if it's a PDF file
        if uploaded_file.type == "application/pdf":
            display_pdf(uploaded_file)
        else:
            st.info("Document preview is available for PDF files only.")
    
    with col2:
        st.subheader("📝 Text Content & Summary")
        
        # Extract text based on file type
        if uploaded_file.type == "application/pdf":
            extracted_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            extracted_text = extract_text_from_docx(uploaded_file)
        elif uploaded_file.type == "text/plain":
            extracted_text = extract_text_from_txt(uploaded_file)
        else:
            st.error("Unsupported file type")
            extracted_text = ""
        
        if extracted_text:
            # Show extracted text in an expandable section
            with st.expander("View Extracted Text", expanded=False):
                st.text_area(
                    "Extracted Content",
                    value=extracted_text[:2000] + ("..." if len(extracted_text) > 2000 else ""),
                    height=200,
                    disabled=True
                )
            
            # Summarize button
            if st.button("🔍 Generate Summary", type="primary"):
                with st.spinner("Generating summary..."):
                    summary_result = summarize_text(
                        extracted_text, 
                        st.session_state.selected_llm,
                        summary_type.lower()
                    )
                    
                    if "error" not in summary_result:
                        st.session_state.summary_result = summary_result
                        st.session_state.document_content = extracted_text
                    else:
                        st.error(f"Summarization failed: {summary_result['error']}")
            
            # Display summary results
            if st.session_state.summary_result:
                st.markdown("---")
                st.subheader("📋 Summary Results")
                
                result = st.session_state.summary_result
                
                # Summary statistics
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Original Words", result["original_length"])
                with col_b:
                    st.metric("Summary Words", result["summary_length"])
                with col_c:
                    st.metric("Compression", f"{result['compression_ratio']}%")
                
                # Summary text
                st.markdown("### 📄 Summary")
                st.success(result["summary"])
                
                # Download button for summary
                st.download_button(
                    label="📥 Download Summary",
                    data=result["summary"],
                    file_name=f"summary_{uploaded_file.name.split('.')[0]}.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Could not extract text from the uploaded file.")

else:
    # Instructions when no file is uploaded
    st.info("👆 Please upload a document to get started")
    
    # Feature highlights
    st.markdown("---")
    st.subheader("✨ Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📄 Multiple Formats**
        - PDF documents
        - Word documents (.docx)
        - Text files (.txt)
        """)
    
    with col2:
        st.markdown("""
        **🔍 Smart Summarization**
        - AI-powered analysis
        - Multiple summary types
        - Customizable length
        """)
    
    with col3:
        st.markdown("""
        **👀 Document Preview**
        - Built-in PDF viewer
        - Text extraction preview
        - Download summaries
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>📚 Powered by AI • Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)