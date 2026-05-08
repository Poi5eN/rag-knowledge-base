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
    
    # Initialize session state (including theme)
    init_session_state()
    
    # Page configuration
    st.set_page_config(
        page_title=Config.APP_TITLE,
        page_icon="assets/image.png",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "RAG Knowledge Base - Chat with your PDFs using AI"
        }
    )
    
    # Inject custom CSS based on theme
    st.html(get_custom_css(st.session_state.theme))
    
    # Helper to load images
    import base64
    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
            
    try:
        ai_icon_b64 = get_base64_image("assets/ai.png")
        icon_html = f'<img src="data:image/png;base64,{ai_icon_b64}" class="header-icon" width="45">'
    except:
        icon_html = "🤖"

    # Top Bar: Notion-style Title and Theme Toggle
    col_header, col_toggle = st.columns([10, 1])
    
    with col_header:
        st.html(f"""
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.5rem;">
    <span style="font-size: 2.5rem;">{Config.APP_ICON}</span>
    <div>
        <h1 style='margin:0; font-weight: 700; font-size: 2rem;'>{Config.APP_TITLE}</h1>
        <p style='color: var(--text-secondary); margin:0; font-size: 0.95rem;'>Think, analyze, and chat with your documents</p>
    </div>
</div>
        """)
            
    with col_toggle:
        # Theme Toggle Button (Top Right)
        current_theme = st.session_state.theme
        btn_text = "🌙" if current_theme == "light" else "☀️" 
        if st.button(btn_text, key="theme_toggle_top", help="Switch Appearance"):
             st.session_state.theme = "dark" if current_theme == "light" else "light"
             st.rerun()

    st.html("<div style='height: 1px; background-color: var(--border-color); margin: 1rem 0 2rem 0; opacity: 0.5;'></div>")
    
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
