"""Main Streamlit application for RAG Knowledge Base."""
import streamlit as st
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.config import Config
from src.utils.session_state import init_session_state
from src.core.vector_store import VectorStore
from src.core.rag_pipeline import RAGPipeline
from src.components.pdf_uploader import render_pdf_uploader
from src.components.sidebar import render_sidebar
from src.components.chat_interface import render_chat_interface, render_welcome_message
from assets.styles import get_custom_css


def main():
    """Main application entry point."""
    
    # Page configuration
    st.set_page_config(
        page_title=Config.APP_TITLE,
        page_icon=Config.APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "RAG Knowledge Base - Chat with your PDFs using AI"
        }
    )
    
    # Inject custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Initialize session state
    init_session_state()
    
    # Header
    st.markdown(f"# {Config.APP_ICON} {Config.APP_TITLE}")
    st.markdown("### Chat with your documents using AI-powered search")
    st.divider()
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        st.error(f"❌ Configuration Error: {str(e)}")
        st.info("👉 Please set your GOOGLE_API_KEY in the .env file")
        st.code("""
# Create a .env file in the project root with:
GOOGLE_API_KEY=your_api_key_here

# Get your free API key from:
# https://makersuite.google.com/app/apikey
        """)
        return
    
    # Initialize core components (cached)
    vector_store = initialize_vector_store()
    rag_pipeline = initialize_rag_pipeline(vector_store)
    
    # Render sidebar
    render_sidebar(vector_store)
    
    # Main content area
    if not st.session_state.documents:
        # Show welcome message and uploader
        render_welcome_message()
        st.divider()
        render_pdf_uploader(vector_store)
    else:
        # Show uploader in a collapsible section
        with st.expander("📤 Upload More Documents", expanded=False):
            render_pdf_uploader(vector_store)
        
        st.divider()
        
        # Show chat interface
        render_chat_interface(rag_pipeline)


@st.cache_resource
def initialize_vector_store():
    """Initialize and cache the vector store."""
    return VectorStore()


@st.cache_resource
def initialize_rag_pipeline(_vector_store):
    """Initialize and cache the RAG pipeline."""
    return RAGPipeline(_vector_store)


if __name__ == "__main__":
    main()
