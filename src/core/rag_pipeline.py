"""RAG pipeline using LangChain and Google Gemini."""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Dict, Any
import streamlit as st
from src.utils.config import Config
from src.core.vector_store import VectorStore


class StreamHandler(BaseCallbackHandler):
    """Callback handler for streaming LLM responses."""
    
    def __init__(self, container):
        self.container = container
        self.text = ""
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Handle new token from LLM."""
        self.text += token
        self.container.markdown(self.text + "▌")


class CustomRetriever:
    """Custom retriever that wraps ChromaDB search."""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
    
    def get_relevant_documents(self, query: str) -> List[Dict]:
        """Retrieve relevant documents for a query."""
        results = self.vector_store.search(query)
        
        # Convert to LangChain document format
        docs = []
        for result in results:
            doc = Document(
                page_content=result["text"],
                metadata=result["metadata"]
            )
            docs.append(doc)
        
        return docs


class RAGPipeline:
    """RAG pipeline for question answering over documents."""
    
    def __init__(self, vector_store: VectorStore):
        """Initialize the RAG pipeline."""
        self.vector_store = vector_store
        self.llm = self._init_llm()
        self.chat_history = []  # Simple list for chat history
        self.retriever = CustomRetriever(vector_store)
    
    def _init_llm(self):
        """Initialize Google Gemini LLM."""
        return ChatGoogleGenerativeAI(
            model=Config.LLM_MODEL,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0.3,
            convert_system_message_to_human=True
        )
    
    def _create_prompt(self) -> PromptTemplate:
        """Create the prompt template."""
        template = """You are a helpful AI assistant that answers questions based on the provided context from uploaded documents.

Context from documents:
{context}

Chat History:
{chat_history}

Question: {question}

Instructions:
1. Answer the question based primarily on the context provided
2. If the context doesn't contain enough information, say so clearly
3. Be concise but comprehensive
4. If relevant, mention which document the information comes from
5. Use a friendly, professional tone

Answer:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "chat_history", "question"]
        )
    
    def query(self, question: str, stream_container=None) -> Dict[str, Any]:
        """
        Query the RAG system.
        
        Args:
            question: User question
            stream_container: Optional Streamlit container for streaming
            
        Returns:
            Dictionary with answer and source documents
        """
        # Get relevant documents
        source_docs = self.retriever.get_relevant_documents(question)
        
        if not source_docs:
            return {
                "answer": "I don't have any documents to answer your question. Please upload some PDFs first.",
                "sources": []
            }
        
        # Create context from retrieved documents
        context = "\n\n".join([doc.page_content for doc in source_docs])
        
        # Format chat history for prompt
        history_text = ""
        for msg in self.chat_history:
            role = msg.get("role", "Human")
            content = msg.get("content", "")
            history_text += f"{role}: {content}\n"
        
        # Create prompt
        prompt = self._create_prompt()
        formatted_prompt = prompt.format(
            context=context,
            chat_history=history_text,
            question=question
        )
        
        # Get answer with streaming if container provided
        if stream_container:
            stream_handler = StreamHandler(stream_container)
            streaming_llm = ChatGoogleGenerativeAI(
                model=Config.LLM_MODEL,
                google_api_key=Config.GOOGLE_API_KEY,
                temperature=0.3,
                streaming=True,
                callbacks=[stream_handler],
                convert_system_message_to_human=True
            )
            answer = streaming_llm.invoke(formatted_prompt).content
        else:
            answer = self.llm.invoke(formatted_prompt).content
        
        # Save to chat history
        self.chat_history.append({"role": "Human", "content": question})
        self.chat_history.append({"role": "AI", "content": answer})
        
        # Format sources
        sources = []
        seen_files = set()
        for doc in source_docs:
            filename = doc.metadata.get("filename", "Unknown")
            if filename not in seen_files:
                sources.append({
                    "filename": filename,
                    "text": doc.page_content[:200] + "..."
                })
                seen_files.add(filename)
        
        return {
            "answer": answer,
            "sources": sources
        }
    
    def clear_memory(self):
        """Clear conversation memory."""
        self.chat_history = []
