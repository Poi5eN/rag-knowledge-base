"""Configuration management for the RAG Knowledge Base application."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    
    # Model Configuration
    LLM_MODEL = "gemini-1.5-flash"  # Primary Google model
    OPENROUTER_MODEL = "openrouter/auto"  # Auto model for OpenRouter
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
        if not Config.GOOGLE_API_KEY and not Config.OPENROUTER_API_KEY:
            raise ValueError(
                "Neither GOOGLE_API_KEY nor OPENROUTER_API_KEY found in environment variables. "
                "Please set at least one of them in .env file or environment."
            )
