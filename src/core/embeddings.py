"""Embedding generation using Sentence Transformers (free local model)."""
from sentence_transformers import SentenceTransformer
from typing import List
import streamlit as st
from src.utils.config import Config


class EmbeddingGenerator:
    """Generate embeddings using local Sentence Transformers model."""
    
    def __init__(self):
        """Initialize the embedding model."""
        self.model = self._load_model()
    
    @st.cache_resource
    def _load_model(_self):
        """Load the sentence transformer model (cached)."""
        return SentenceTransformer(Config.EMBEDDING_MODEL)
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text string to embed
            
        Returns:
            Embedding vector
        """
        embedding = self.model.encode([text], show_progress_bar=False)
        return embedding[0].tolist()
