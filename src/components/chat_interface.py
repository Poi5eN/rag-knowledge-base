"""Chat interface component with streaming responses."""
import streamlit as st
from typing import Dict, Any
from src.core.rag_pipeline import RAGPipeline
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
         with st.chat_message("assistant"):
            response_container = st.empty()
            
            # Custom Thinking Animation (Neural Pulse)
            thinking_placeholder = st.empty()
            thinking_placeholder.markdown("""
                <div class="thinking-container">
                    <div class="neural-dots">
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                    </div>
                    <div class="thinking-text">Resolving query...</div>
                </div>
            """, unsafe_allow_html=True)
            
            try:
                last_user_msg = st.session_state.messages[-1]["content"]
                result = rag_pipeline.query(last_user_msg)
                
                # Clear thinking animation
                thinking_placeholder.empty()
                
                response_container.markdown(result["answer"])
                add_message("assistant", result["answer"], result.get("sources"), result.get("reasoning"))
                st.rerun()
            except Exception as e:
                 thinking_placeholder.empty()
                 st.error(f"Error: {e}")

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message
        add_message("user", prompt)
        st.rerun() # Rerun to trigger the generation block above


def render_welcome_message():
    """Render welcome message when no documents are uploaded."""
    import base64
    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
            
    try:
        logo_b64 = get_base64_image("assets/image.png")
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img" width="90">'
    except:
        logo_html = "🧠"

    st.markdown(f"""
    <div style='text-align: center; margin-top: 2rem;'>
        {logo_html}
        <h2 style='font-size: 2rem; font-weight: 600; margin-bottom: 0.5rem; margin-top: 1rem;'>Welcome to RAG Knowledge Base</h2>
        <p style='font-size: 1.1rem; color: var(--text-secondary); margin-top: 0.5rem;'>
            Upload PDFs and chat with an intelligent agent
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px;'>
            <h3 style='margin: 0 0 0.5rem 0; color: var(--text-color) !important; font-size: 1.2rem !important;'>📤</h3>
            <h4 style='margin: 0 0 0.5rem 0; color: var(--text-color) !important;'>Upload</h4>
            <p style='margin: 0; color: var(--text-secondary); font-size: 0.9rem;'>Upload multiple PDF documents</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px;'>
            <h3 style='margin: 0 0 0.5rem 0; color: var(--text-color) !important; font-size: 1.2rem !important;'>🧠</h3>
            <h4 style='margin: 0 0 0.5rem 0; color: var(--text-color) !important;'>AI Analysis</h4>
            <p style='margin: 0; color: var(--text-secondary); font-size: 0.9rem;'>Powered by Google Gemini</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px;'>
            <h3 style='margin: 0 0 0.5rem 0; color: var(--text-color) !important; font-size: 1.2rem !important;'>💬</h3>
            <h4 style='margin: 0 0 0.5rem 0; color: var(--text-color) !important;'>Chat</h4>
            <p style='margin: 0; color: var(--text-secondary); font-size: 0.9rem;'>Get instant answers & citations</p>
        </div>
        """, unsafe_allow_html=True)
