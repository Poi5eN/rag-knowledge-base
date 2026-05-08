"""ChromaDB vector store integration."""
import chromadb
from chromadb.config import Settings
from typing import List, Dict
import streamlit as st
from src.utils.config import Config
from src.core.embeddings import EmbeddingGenerator


class VectorStore:
    """Manage ChromaDB vector store for document retrieval."""
    
    def __init__(self):
        """Initialize ChromaDB client and collection."""
        self.embedding_generator = EmbeddingGenerator()
        self.client = self._init_client()
        self.collection = self._get_or_create_collection()
    
    @st.cache_resource
    def _init_client(_self):
        """Initialize ChromaDB client (cached)."""
        return chromadb.PersistentClient(
            path=Config.CHROMA_PERSIST_DIR,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
    
    def _get_or_create_collection(self):
        """Get or create the collection."""
        try:
            return self.client.get_or_create_collection(
                name=Config.COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            raise Exception(f"Error creating collection: {str(e)}")
    
    def add_documents(self, documents: List[Dict], progress_callback=None):
        """
        Add documents to the vector store.
        
        Args:
            documents: List of document dictionaries with 'text' and 'metadata'
            progress_callback: Optional callback function for progress updates
        """
        texts = [doc["text"] for doc in documents]
        texts = [doc["text"] for doc in documents]
        
        # Sanitize metadata (ChromaDB requires primitives)
        metadatas = []
        for doc in documents:
            clean_meta = {}
            for k, v in doc["metadata"].items():
                if isinstance(v, list):
                    clean_meta[k] = ", ".join(str(i) for i in v)
                elif v is None:
                    clean_meta[k] = ""
                else:
                    clean_meta[k] = v
            metadatas.append(clean_meta)
        
        # Generate unique IDs
        ids = [f"{doc['metadata']['filename']}_{doc['metadata']['chunk_id']}" 
               for doc in documents]
        
        # Generate embeddings
        if progress_callback:
            progress_callback(0.3, "Generating embeddings...")
        
        embeddings = self.embedding_generator.generate_embeddings(texts)
        
        # Add to ChromaDB
        if progress_callback:
            progress_callback(0.7, "Storing in vector database...")
        
        self.collection.upsert(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        if progress_callback:
            progress_callback(1.0, "Complete!")
    
    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant documents with metadata and scores
        """
        if top_k is None:
            top_k = Config.TOP_K_RESULTS
        
        # Generate query embedding
        query_embedding = self.embedding_generator.generate_embedding(query)
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        documents = []
        if results and results['documents'] and len(results['documents']) > 0:
            for i in range(len(results['documents'][0])):
                doc = {
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "score": 1 - results['distances'][0][i]  # Convert distance to similarity
                }
                documents.append(doc)
        
        return documents
    
    def delete_by_filename(self, filename: str):
        """
        Delete all chunks for a specific file.
        
        Args:
            filename: Name of the file to delete
        """
        # Get all documents
        all_docs = self.collection.get()
        
        # Find IDs to delete
        ids_to_delete = [
            doc_id for doc_id, metadata in zip(all_docs['ids'], all_docs['metadatas'])
            if metadata.get('filename') == filename
        ]
        
        # Delete
        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)
    
    def clear_all(self):
        """Delete all documents from the collection."""
        try:
            self.client.delete_collection(name=Config.COLLECTION_NAME)
            self.collection = self._get_or_create_collection()
        except Exception as e:
            raise Exception(f"Error clearing collection: {str(e)}")
    
    def get_document_count(self) -> int:
        """Get the total number of document chunks."""
        return self.collection.count()
