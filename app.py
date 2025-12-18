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
    st.markdown(get_custom_css(st.session_state.theme), unsafe_allow_html=True)
    
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

    # Top Bar: Title (Left) and Theme Toggle (Right)
    col_header, col_toggle = st.columns([6, 1])
    
    with col_header:
        # Header with AI Icon using Flexbox for perfect alignment
        st.markdown(f"""
            <div class="header-container">
                {icon_html}
                <h1 style='margin:0; padding:0; display:inline-block; vertical-align:middle;'>{Config.APP_TITLE}</h1>
            </div>
        """, unsafe_allow_html=True)
            
    with col_toggle:
        # Theme Toggle Button
        current_theme = st.session_state.theme
        btn_text = "🌙" if current_theme == "light" else "☀️" 
        if st.button(btn_text, key="theme_toggle_top", help="Switch Theme", use_container_width=True):
             new_theme = "dark" if current_theme == "light" else "light"
             st.session_state.theme = new_theme
             st.rerun()

    st.markdown("<p style='color: var(--text-secondary); margin-top: -10px; margin-bottom: 2rem;'>Chat with your documents using AI-powered search</p>", unsafe_allow_html=True)
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
