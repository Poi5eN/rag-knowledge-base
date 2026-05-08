"""Document management sidebar."""
# pyrefly: ignore [missing-import]
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
        # Helper to load images
        import base64
        def get_base64_image(image_path):
            try:
                with open(image_path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
            except Exception:
                return ""

        logo_b64 = get_base64_image("assets/image.png")
        if logo_b64:
            logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img" width="100">'
        else:
            logo_html = "🧠"

        # Centered Layout for Logo
        st.html(f"""
            <div class="sidebar-content">
                {logo_html}
                <h3 style="margin-top: 15px; margin-bottom: 0;">RAG Knowledge Base</h3>
            </div>
        """)
        
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
                        
                        # Show X-Ray Tags
                        if "topics" in doc:
                            topics = doc["topics"][:3] # Show max 3 topics
                            # Create simple badge style using markdown
                            badges = " ".join([f"`{t}`" for t in topics])
                            st.markdown(badges)
                        if "doc_type" in doc:
                            st.caption(f"_{doc['doc_type']}_")
                    
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
        
        # Suggested Questions (Helpful Feature)
        if st.session_state.get("doc_faqs"):
            st.markdown("### 💡 Suggested Questions")
            for faq in st.session_state.doc_faqs[:5]:
                if st.button(faq, key=f"faq_{faq}", use_container_width=True):
                    # We can't easily trigger the chat input from here, but we can set a session state variable
                    st.session_state.current_prompt = faq
                    st.rerun()
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
