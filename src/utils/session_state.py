"""Session state management for Streamlit application."""
import streamlit as st


def init_session_state():
    """Initialize all session state variables."""
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Uploaded documents
    if "documents" not in st.session_state:
        st.session_state.documents = []
    
    # Vector store initialization flag
    if "vector_store_ready" not in st.session_state:
        st.session_state.vector_store_ready = False
    
    # Processing status
    if "processing" not in st.session_state:
        st.session_state.processing = False
    
    # Current document being processed
    if "current_doc" not in st.session_state:
        st.session_state.current_doc = None
    
    # UI Theme (Default to Light for Notion vibe)
    if "theme" not in st.session_state:
        st.session_state.theme = "light"


def set_theme(theme: str):
    """Set the UI theme."""
    st.session_state.theme = theme


def add_message(role: str, content: str, sources: list = None, reasoning: str = None):
    """Add a message to chat history."""
    message = {
        "role": role,
        "content": content,
    }
    if sources:
        message["sources"] = sources
    if reasoning:
        message["reasoning"] = reasoning
    st.session_state.messages.append(message)


def clear_chat_history():
    """Clear all chat messages."""
    st.session_state.messages = []


def add_document(filename: str, num_pages: int, metadata: dict = None):
    """Add a document to the uploaded documents list."""
    doc = {
        "filename": filename,
        "num_pages": num_pages
    }
    if metadata:
        doc.update(metadata)
    st.session_state.documents.append(doc)


def remove_document(filename: str):
    """Remove a document from the uploaded documents list."""
    st.session_state.documents = [
        doc for doc in st.session_state.documents 
        if doc["filename"] != filename
    ]


def clear_all_documents():
    """Clear all uploaded documents."""
    st.session_state.documents = []
    st.session_state.vector_store_ready = False
