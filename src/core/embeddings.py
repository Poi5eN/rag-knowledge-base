# pyrefly: ignore [missing-import]
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List
# pyrefly: ignore [missing-import]
import streamlit as st
from src.utils.config import Config


class EmbeddingGenerator:
    """Generate embeddings using local Sentence Transformers model."""
    
    def __init__(self):
        """Initialize the embedding model."""
        self.model = self._load_model()
    
    @st.cache_resource
    def _load_model(_self):
        """Load the Google embeddings model (cached)."""
        return GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=Config.GOOGLE_API_KEY
        )
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Google's API.
        """
        return self.model.embed_documents(texts)
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        """
        return self.model.embed_query(text)
