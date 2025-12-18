"""PDF processing and text extraction."""
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict
import streamlit as st
from src.utils.config import Config


class PDFProcessor:
    """Handle PDF processing, text chunking, and metadata extraction."""
    
    def __init__(self):
        """Initialize the PDF processor."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
    def generate_xray_metadata(self, text_sample: str) -> Dict:
        """
        Generate 'X-Ray' metadata (topics, type) using Gemini Flash.
        Uses the first few pages of text to categorize the document.
        """
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.prompts import PromptTemplate
            
            llm = ChatGoogleGenerativeAI(
                model=Config.LLM_MODEL,
                google_api_key=Config.GOOGLE_API_KEY,
                temperature=0.0
            )
            
            prompt = PromptTemplate(
                template="""Analyze the following document text and extract key metadata and frequently asked questions.
                
                Text Sample:
                {text}
                
                Return ONLY a valid JSON object with these keys:
                - "topics": [list of 3-5 key topics/themes]
                - "doc_type": "Research Paper" or "Technical Report" or "Textbook" or "Contract" or "Other"
                - "summary": "1 sentence brief summary"
                - "faqs": [list of 5 questions that can be answered by this document]
                
                JSON:""",
                input_variables=["text"]
            )
            
            chain = prompt | llm
            response = chain.invoke({"text": text_sample[:3000]})
            
            # Clean up response to get pure JSON
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
                
            import json
            return json.loads(content)
        except Exception as e:
            print(f"Error generating X-Ray metadata: {e}")
            return {"topics": ["General"], "doc_type": "Document", "summary": "No summary available", "faqs": []}

    def process_pdf(self, pdf_file, filename: str) -> List[Dict]:
        """
        Process a PDF file: extract text page-by-page, create chunks with page numbers,
        and generate document-level X-Ray metadata.
        """
        try:
            pdf_reader = PdfReader(pdf_file)
            all_chunks = []
            full_text_for_xray = ""
            
            # 1. Extract text page by page and chunk immediately
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if not page_text:
                    continue
                
                # Accumulate first few pages for X-Ray analysis
                if page_num < 3:
                    full_text_for_xray += page_text + "\n"
                
                # Split this page's text
                page_chunks = self.text_splitter.split_text(page_text)
                
                for i, chunk in enumerate(page_chunks):
                    all_chunks.append({
                        "text": chunk,
                        "metadata": {
                            "filename": filename,
                            "source": filename,
                            "page": page_num + 1,  # 1-indexed for display
                            "chunk_id": len(all_chunks) + i
                        }
                    })
            
            # 2. Generate X-Ray Metadata (Topics, Summary)
            xray_data = self.generate_xray_metadata(full_text_for_xray)
            
            # 3. Enrich all chunks with X-Ray data (denormalized for retrieval filtering if needed)
            # And also return the doc-level metadata separately?
            # For now, we'll attach it to every chunk so it's available in the VectorStore results
            for chunk in all_chunks:
                chunk["metadata"].update(xray_data)
                
            return all_chunks
            
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    def get_pdf_page_count(self, pdf_file) -> int:
        """Get the number of pages in a PDF."""
        try:
            pdf_reader = PdfReader(pdf_file)
            return len(pdf_reader.pages)
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
