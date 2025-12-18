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


def add_message(role: str, content: str, sources: list = None):
    """Add a message to chat history."""
    message = {
        "role": role,
        "content": content,
    }
    if sources:
        message["sources"] = sources
    st.session_state.messages.append(message)


def clear_chat_history():
    """Clear all chat messages."""
    st.session_state.messages = []


def add_document(filename: str, num_pages: int):
    """Add a document to the uploaded documents list."""
    st.session_state.documents.append({
        "filename": filename,
        "num_pages": num_pages
    })


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
