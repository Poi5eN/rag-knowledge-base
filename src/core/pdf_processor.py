"""PDF processing and text extraction."""
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict
import streamlit as st
from src.utils.config import Config


class PDFProcessor:
    """Handle PDF processing and text chunking."""
    
    def __init__(self):
        """Initialize the PDF processor."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """
        Extract all text from a PDF file.
        
        Args:
            pdf_file: Uploaded PDF file object
            
        Returns:
            Extracted text as a string
        """
        try:
            pdf_reader = PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def get_pdf_page_count(self, pdf_file) -> int:
        """
        Get the number of pages in a PDF.
        
        Args:
            pdf_file: Uploaded PDF file object
            
        Returns:
            Number of pages
        """
        try:
            pdf_reader = PdfReader(pdf_file)
            return len(pdf_reader.pages)
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Split text into chunks with metadata.
        
        Args:
            text: Text to split
            metadata: Optional metadata to attach to each chunk
            
        Returns:
            List of dictionaries containing chunks and metadata
        """
        chunks = self.text_splitter.split_text(text)
        
        documents = []
        for i, chunk in enumerate(chunks):
            doc = {
                "text": chunk,
                "metadata": {
                    **(metadata or {}),
                    "chunk_id": i,
                    "total_chunks": len(chunks)
                }
            }
            documents.append(doc)
        
        return documents
    
    def process_pdf(self, pdf_file, filename: str) -> List[Dict]:
        """
        Process a PDF file: extract text and create chunks.
        
        Args:
            pdf_file: Uploaded PDF file object
            filename: Name of the PDF file
            
        Returns:
            List of document chunks with metadata
        """
        # Extract text
        text = self.extract_text_from_pdf(pdf_file)
        
        # Create chunks with metadata
        metadata = {
            "filename": filename,
            "source": filename
        }
        
        chunks = self.chunk_text(text, metadata)
        
        return chunks
