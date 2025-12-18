"""PDF upload component with beautiful UI."""
import streamlit as st
from typing import List
from src.core.pdf_processor import PDFProcessor
from src.core.vector_store import VectorStore
from src.utils.session_state import add_document
from src.utils.config import Config


def render_pdf_uploader(vector_store: VectorStore):
    """
    Render the PDF upload interface.
    
    Args:
        vector_store: VectorStore instance
    """
    st.markdown("### 📄 Upload Documents")
    st.markdown("Upload PDF documents to chat with them using AI")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help=f"Upload PDF files (max {Config.MAX_FILE_SIZE_MB}MB each)"
    )
    
    if uploaded_files:
        if st.button("🚀 Process Documents", use_container_width=True, type="primary"):
            process_pdfs(uploaded_files, vector_store)


def process_pdfs(uploaded_files: List, vector_store: VectorStore):
    """
    Process uploaded PDF files.
    
    Args:
        uploaded_files: List of uploaded file objects
        vector_store: VectorStore instance
    """
    processor = PDFProcessor()
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_files = len(uploaded_files)
    all_documents = []
    
    try:
        for idx, uploaded_file in enumerate(uploaded_files):
            # Update progress
            file_progress = idx / total_files
            progress_bar.progress(file_progress)
            status_text.info(f"📖 Processing {uploaded_file.name}...")
            
            # Check file size
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > Config.MAX_FILE_SIZE_MB:
                st.error(f"❌ {uploaded_file.name} is too large ({file_size_mb:.1f}MB). Max size: {Config.MAX_FILE_SIZE_MB}MB")
                continue
            
            # Get page count
            num_pages = processor.get_pdf_page_count(uploaded_file)
            
            # Reset file pointer
            uploaded_file.seek(0)
            
            # Process PDF
            chunks = processor.process_pdf(uploaded_file, uploaded_file.name)
            all_documents.extend(chunks)
            
            # Extract generated FAQs and Metadata
            if chunks and "faqs" in chunks[0]["metadata"]:
                new_faqs = chunks[0]["metadata"]["faqs"]
                if "doc_faqs" not in st.session_state:
                    st.session_state.doc_faqs = []
                # Add unique FAQs
                for faq in new_faqs:
                    if faq not in st.session_state.doc_faqs:
                        st.session_state.doc_faqs.append(faq)
                        
            # Extract metadata for session state
            doc_metadata = {}
            if chunks and "metadata" in chunks[0]:
                 # Get X-Ray data from first chunk
                 meta = chunks[0]["metadata"]
                 if "topics" in meta:
                     doc_metadata["topics"] = meta["topics"]
                 if "doc_type" in meta:
                     doc_metadata["doc_type"] = meta["doc_type"]
            
            # Add to session state
            add_document(uploaded_file.name, num_pages, doc_metadata)
        
        # Add all documents to vector store
        if all_documents:
            def update_progress(progress, message):
                progress_bar.progress(progress)
                status_text.info(message)
            
            status_text.info("🔮 Generating embeddings and storing documents...")
            vector_store.add_documents(all_documents, progress_callback=update_progress)
            
            # Mark vector store as ready
            st.session_state.vector_store_ready = True
            
            # Success message
            progress_bar.progress(1.0)
            status_text.success(f"✅ Successfully processed {total_files} document(s)!")
            
            if "doc_faqs" in st.session_state and st.session_state.doc_faqs:
                st.toast(f"🎉 Generated {len(st.session_state.doc_faqs)} smart questions!", icon="💡")
            
            st.balloons()
            
            # Clear after 2 seconds
            import time
            time.sleep(2)
            progress_bar.empty()
            status_text.empty()
            st.rerun() # Rerun to update sidebar and chat
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ Error processing documents: {str(e)}")
