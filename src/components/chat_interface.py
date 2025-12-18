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
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show sources if available
                if "sources" in message and message["sources"]:
                    with st.expander("📚 Sources"):
                        for source in message["sources"]:
                            st.markdown(f"**{source['filename']}**")
                            st.caption(source['text'])
                            st.divider()
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message
        add_message("user", prompt)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            response_container = st.empty()
            
            # Show thinking animation
            with st.spinner("🤔 Thinking..."):
                try:
                    # Query RAG pipeline with streaming
                    result = rag_pipeline.query(prompt, stream_container=response_container)
                    
                    # Clear the streaming placeholder and show final answer
                    response_container.markdown(result["answer"])
                    
                    # Add assistant message
                    add_message("assistant", result["answer"], result.get("sources"))
                    
                    # Show sources
                    if result.get("sources"):
                        with st.expander("📚 Sources", expanded=False):
                            for source in result["sources"]:
                                st.markdown(f"**📄 {source['filename']}**")
                                st.caption(source['text'])
                                st.divider()
                
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    response_container.error(error_msg)
                    add_message("assistant", error_msg)


def render_welcome_message():
    """Render welcome message when no documents are uploaded."""
    st.markdown("""
    <div style='text-align: center; padding: 3rem 1rem;'>
        <h1 style='font-size: 3rem; margin-bottom: 1rem;'>🧠</h1>
        <h2>Welcome to RAG Knowledge Base</h2>
        <p style='font-size: 1.2rem; color: #64748b; margin-top: 1rem;'>
            Upload PDF documents and chat with them using AI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 1rem; color: white;'>
            <h3 style='margin: 0 0 0.5rem 0;'>📤</h3>
            <h4 style='margin: 0 0 0.5rem 0;'>Upload</h4>
            <p style='margin: 0; opacity: 0.9; font-size: 0.9rem;'>Upload multiple PDF documents</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 1rem; color: white;'>
            <h3 style='margin: 0 0 0.5rem 0;'>🤖</h3>
            <h4 style='margin: 0 0 0.5rem 0;'>AI Analysis</h4>
            <p style='margin: 0; opacity: 0.9; font-size: 0.9rem;'>Powered by Google Gemini</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 1rem; color: white;'>
            <h3 style='margin: 0 0 0.5rem 0;'>💬</h3>
            <h4 style='margin: 0 0 0.5rem 0;'>Chat</h4>
            <p style='margin: 0; opacity: 0.9; font-size: 0.9rem;'>Get instant answers</p>
        </div>
        """, unsafe_allow_html=True)
