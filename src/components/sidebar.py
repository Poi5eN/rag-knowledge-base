"""Document management sidebar."""
import streamlit as st
from src.core.vector_store import VectorStore
from src.utils.session_state import remove_document, clear_all_documents, clear_chat_history


def render_sidebar(vector_store: VectorStore):
    """
    Render the sidebar with document management.
    
    Args:
        vector_store: VectorStore instance
    """
    with st.sidebar:
        st.markdown("## 📚 Document Library")
        
        # Show uploaded documents
        if st.session_state.documents:
            st.markdown(f"**{len(st.session_state.documents)} Document(s) Uploaded**")
            
            # Show each document
            for idx, doc in enumerate(st.session_state.documents):
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"📄 **{doc['filename']}**")
                        st.caption(f"{doc['num_pages']} pages")
                    
                    with col2:
                        if st.button("🗑️", key=f"delete_{idx}_{doc['filename']}", help="Delete document"):
                            delete_document(doc['filename'], vector_store)
                            st.rerun()
                    
                    st.divider()
            
            # Clear all button
            if st.button("🗑️ Clear All Documents", use_container_width=True, type="secondary"):
                if st.session_state.get("confirm_clear", False):
                    clear_all_documents()
                    vector_store.clear_all()
                    clear_chat_history()
                    st.session_state.confirm_clear = False
                    st.success("All documents cleared!")
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("Click again to confirm deletion")
        
        else:
            st.info("No documents uploaded yet")
        
        st.divider()
        
        # Vector store stats
        if st.session_state.vector_store_ready:
            chunk_count = vector_store.get_document_count()
            st.markdown("### 📊 Vector Store Stats")
            st.metric("Total Chunks", chunk_count)
        
        st.divider()
        
        # Chat controls
        st.markdown("### 💬 Chat Controls")
        if st.button("🧹 Clear Chat History", use_container_width=True):
            clear_chat_history()
            st.success("Chat history cleared!")
            st.rerun()
        
        st.divider()
        
        # Info section
        st.markdown("### ℹ️ About")
        st.markdown("""
        This RAG Knowledge Base allows you to:
        - 📤 Upload PDF documents
        - 💬 Chat with your documents
        - 🔍 Get AI-powered answers
        - 📚 Manage your library
        
        **Tech Stack:**
        - 🤖 Google Gemini AI
        - 🗄️ ChromaDB Vector Store
        - 🧠 Sentence Transformers
        - ⚡ Streamlit
        """)
        
        st.divider()
        
        # GitHub link (if you want to add)
        st.markdown("Built with ❤️ for YC Recruiters")


def delete_document(filename: str, vector_store: VectorStore):
    """
    Delete a document from the vector store and session state.
    
    Args:
        filename: Name of the document to delete
        vector_store: VectorStore instance
    """
    try:
        # Remove from vector store
        vector_store.delete_by_filename(filename)
        
        # Remove from session state
        remove_document(filename)
        
        # Check if any documents left
        if not st.session_state.documents:
            st.session_state.vector_store_ready = False
        
        st.success(f"Deleted {filename}")
    except Exception as e:
        st.error(f"Error deleting document: {str(e)}")
