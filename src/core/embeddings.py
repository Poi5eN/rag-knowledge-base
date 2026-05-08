from typing import List
# pyrefly: ignore [missing-import]
import streamlit as st
import time
# pyrefly: ignore [missing-import]
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# pyrefly: ignore [missing-import]
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.utils.config import Config

class EmbeddingGenerator:
    """Generate embeddings with Google API and local fallback for resilience."""
    
    def __init__(self):
        """Initialize both cloud and local models."""
        self.cloud_model = self._load_cloud_model()
        self.local_model = self._load_local_model()
    
    @st.cache_resource
    def _load_cloud_model(_self):
        """Load Google embeddings model (cached)."""
        try:
            return GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001",
                google_api_key=Config.GOOGLE_API_KEY,
                task_type="retrieval_document"
            )
        except Exception:
            return None

    @st.cache_resource
    def _load_local_model(_self):
        """Load local sentence-transformers model as a fallback (cached)."""
        try:
            return HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
        except Exception:
            return None

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        Tries Google API first, then falls back to local model if quota is hit.
        """
        if not texts:
            return []

        # Try Google API first
        if self.cloud_model:
            try:
                # We'll batch them manually to be safer with rate limits
                batch_size = 50
                all_embeddings = []
                
                for i in range(0, len(texts), batch_size):
                    batch = texts[i:i + batch_size]
                    try:
                        batch_embeddings = self.cloud_model.embed_documents(batch)
                        all_embeddings.extend(batch_embeddings)
                    except Exception as e:
                        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                             print(f"Cloud API limit reached, switching to local model for remaining chunks...")
                             # Fallback to local for the rest of this request
                             remaining_texts = texts[i:]
                             remaining_embeddings = self.local_model.embed_documents(remaining_texts)
                             all_embeddings.extend(remaining_embeddings)
                             return all_embeddings
                        else:
                            raise e
                return all_embeddings
            except Exception as e:
                print(f"Cloud embedding error: {e}. Falling back to local model.")
        
        # Fallback to local model
        if self.local_model:
            return self.local_model.embed_documents(texts)
        
        raise ValueError("No embedding models available (cloud or local).")

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        """
        try:
            if self.cloud_model:
                return self.cloud_model.embed_query(text)
        except Exception:
            pass
            
        if self.local_model:
            return self.local_model.embed_query(text)
            
        raise ValueError("No embedding models available.")
