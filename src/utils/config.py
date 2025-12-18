"""Configuration management for the RAG Knowledge Base application."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # Model Configuration
    LLM_MODEL = "gemini-2.5-flash"  # Stable model as of Dec 2025 (GA: June 17, 2025)
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Free local model
    
    # ChromaDB Configuration
    CHROMA_PERSIST_DIR = "./chroma_db"
    COLLECTION_NAME = "rag_documents"
    
    # Chunking Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Retrieval Configuration
    TOP_K_RESULTS = 4
    
    # UI Configuration
    APP_TITLE = "RAG Knowledge Base"
    APP_ICON = "🧠"
    MAX_FILE_SIZE_MB = 10
    
    @staticmethod
    def validate():
        """Validate required configuration."""
        if not Config.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY not found in environment variables. "
                "Please set it in .env file or environment."
            )
