"""Chat interface component with streaming responses."""
# pyrefly: ignore [missing-import]
import streamlit as st
from typing import Dict, Any
from src.core.rag_pipeline import RAGPipeline
from src.utils.config import Config
from src.utils.session_state import add_message


def render_chat_interface(rag_pipeline: RAGPipeline):
    """
    Render the chat interface.
    
    Args:
        rag_pipeline: RAGPipeline instance
    """
    st.markdown("### 💬 Chat with Your Documents")
    
    # Check if documents are uploaded
    if not st.session_state.vector_store_ready:
        st.info("👆 Please upload some PDF documents to start chatting!")
        return
    
    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        if not st.session_state.messages and "doc_faqs" in st.session_state and st.session_state.doc_faqs:
             st.markdown("### 💡 Suggested Questions")
             cols = st.columns(2)
             for i, faq in enumerate(st.session_state.doc_faqs[:4]): # Show max 4
                 if cols[i % 2].button(faq, use_container_width=True):
                     # Hack to trigger chat with this question
                     add_message("user", faq)
                     st.rerun()

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show reasoning if available
                if "reasoning" in message and message["reasoning"]:
                    with st.status("🧠 Thinking Process", state="complete", expanded=False):
                        st.markdown(message["reasoning"])
                
                # Show sources if available
                if "sources" in message and message["sources"]:
                    with st.expander("📚 Sources"):
                        for source in message["sources"]:
                            st.markdown(f"**{source['filename']}** (Page {source.get('page', '?')})")
                            st.caption(source['text'])
                            st.divider()
    
    # Simple logic to handle the "Rerun" case where we added a user message but haven't generated response yet
    # Check if last message is user, if so, generate response
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                with st.chat_message("assistant", avatar="🤖"):
                    # Show a subtle pulsing "Thinking" indicator
                    with st.container():
                        st.html("""
<div class="thinking-container" style="background: transparent; border: none; padding: 0;">
    <div class="neural-dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
    <span class="thinking-text" style="font-style: italic;">Consulting your documents...</span>
</div>
                        """)
                        
                        try:
                            last_user_msg = st.session_state.messages[-1]["content"]
                            result = rag_pipeline.query(last_user_msg)
                            st.rerun()
                        except Exception as e:
                             st.error(f"Error: {e}")

    # Chat input
    prompt = st.chat_input("Ask a question about your documents...")
    
    # Handle suggested questions from sidebar
    if st.session_state.get("current_prompt"):
        prompt = st.session_state.current_prompt
        del st.session_state.current_prompt
        
    if prompt:
        # Add user message
        add_message("user", prompt)
        st.rerun() # Rerun to trigger the generation block above


def render_welcome_message():
    """Render the landing page welcome message."""
    st.html(f"""
<div class="welcome-container" style="animation: fadeIn 0.8s ease-out;">
    <div style="font-size: 5rem; margin-bottom: 1rem;">{Config.APP_ICON}</div>
    <h2 style="font-size: 2.5rem; margin-bottom: 0.5rem;">Welcome to your Knowledge Base</h2>
    <p style="color: var(--text-secondary); font-size: 1.1rem; max-width: 600px; margin-bottom: 3rem;">
        A minimal, AI-powered system to transform your PDFs into an interactive brain. 
        Upload documents to get started.
    </p>
    
    <div class="doc-gallery" style="width: 100%; max-width: 900px;">
        <div class="notion-card">
            <div style="font-size: 2rem; margin-bottom: 1rem;">📤</div>
            <h4 style="margin-bottom: 0.5rem;">Upload</h4>
            <p style="font-size: 0.9rem; color: var(--text-secondary);">Bring your PDFs, research papers, or manuals.</p>
        </div>
        <div class="notion-card">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🧠</div>
            <h4 style="margin-bottom: 0.5rem;">AI Analysis</h4>
            <p style="font-size: 0.9rem; color: var(--text-secondary);">Automatic topic detection and summary extraction.</p>
        </div>
        <div class="notion-card">
            <div style="font-size: 2rem; margin-bottom: 1rem;">💬</div>
            <h4 style="margin-bottom: 0.5rem;">Chat</h4>
            <p style="font-size: 0.9rem; color: var(--text-secondary);">Ask questions and get answers with citations.</p>
        </div>
    </div>
</div>
    """)
