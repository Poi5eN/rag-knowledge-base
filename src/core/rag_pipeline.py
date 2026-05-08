"""RAG pipeline using LangChain and Google Gemini."""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
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
    
    def _init_llm(self, streaming=False, callbacks=None):
        """Initialize LLM with OpenRouter as primary and Gemini as fallback."""
        llms = []
        
        # 1. Primary: OpenRouter
        if Config.OPENROUTER_API_KEY:
            primary_llm = ChatOpenAI(
                model=Config.OPENROUTER_MODEL,
                openai_api_key=Config.OPENROUTER_API_KEY,
                openai_api_base="https://openrouter.ai/api/v1",
                temperature=0.3,
                streaming=streaming,
                callbacks=callbacks,
                default_headers={
                    "HTTP-Referer": "https://github.com/rag-knowledge-base",
                    "X-Title": "RAG Knowledge Base"
                }
            )
            llms.append(primary_llm)
            
        # 2. Fallback: Google Gemini
        if Config.GOOGLE_API_KEY:
            fallback_llm = ChatGoogleGenerativeAI(
                model=Config.LLM_MODEL,
                google_api_key=Config.GOOGLE_API_KEY,
                temperature=0.3,
                streaming=streaming,
                callbacks=callbacks,
                convert_system_message_to_human=True
            )
            llms.append(fallback_llm)
            
        if not llms:
            raise ValueError("No LLM API keys provided. Please check your .env file.")
            
        # Create chain with fallback if multiple providers available
        if len(llms) > 1:
            return llms[0].with_fallbacks(llms[1:])
        return llms[0]
    
    def _create_prompt(self) -> PromptTemplate:
        """Create the prompt template with CoT instructions."""
        template = """You are an intelligent AI assistant provided with context from documents.

Context:
{context}

Chat History:
{chat_history}

Question: {question}

Instructions:
1. First, think step-by-step about how to answer the question based on the context. Enclose your thinking process in <thinking> tags.
2. If the context doesn't contain the answer, say so clearly.
3. Provide a clear, professional answer after the thinking tags.
4. Cite the source document names if available.

Answer:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "chat_history", "question"]
        )
    
    def query(self, question: str, stream_container=None) -> Dict[str, Any]:
        """
        Query the RAG system with CoT support.
        """
        # Get relevant documents
        source_docs = self.retriever.get_relevant_documents(question)
        
        if not source_docs:
            return {
                "answer": "I don't have enough information in the uploaded documents to answer that. Please upload more documents.",
                "reasoning": "No relevant documents found in the vector store.",
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
        
        # Get answer
        # Note: Streaming with thought tags is tricky. We'll stream the raw output
        # and let the UI handle the tag parsing or just show raw stream and then clean up.
        # For better UX, we might disable streaming for CoT or use a sophisticated parser.
        # Let's keep streaming but we'll return the full parsed response at the end.
        
        full_response = ""
        if stream_container:
            stream_handler = StreamHandler(stream_container)
            # Create a simple callback to accumulate text properly since stream_handler 
            # might not capture everything if we are doing complex logic
            streaming_llm = self._init_llm(streaming=True, callbacks=[stream_handler])
            # We invoke and get the full response wrapper
            response_obj = streaming_llm.invoke(formatted_prompt)
            full_response = response_obj.content
        else:
            response_obj = self.llm.invoke(formatted_prompt)
            full_response = response_obj.content
        
        # Parse Thinking vs Answer
        import re
        reasoning = ""
        answer = full_response
        
        thinking_match = re.search(r"<thinking>(.*?)</thinking>", full_response, re.DOTALL)
        if thinking_match:
            reasoning = thinking_match.group(1).strip()
            # Remove thinking tags from answer
            answer = re.sub(r"<thinking>.*?</thinking>", "", full_response, flags=re.DOTALL).strip()
        
        # Save to chat history (save clean answer)
        self.chat_history.append({"role": "Human", "content": question})
        self.chat_history.append({"role": "AI", "content": answer})
        
        # Format sources with page numbers if available
        sources = []
        seen_sources = set()
        for doc in source_docs:
            filename = doc.metadata.get("filename", "Unknown")
            page_num = doc.metadata.get("page", "?")
            source_key = f"{filename}_p{page_num}"
            
            if source_key not in seen_sources:
                sources.append({
                    "filename": filename,
                    "page": page_num,
                    "text": doc.page_content[:200] + "..."
                })
                seen_sources.add(source_key)
        
        return {
            "answer": answer,
            "reasoning": reasoning,
            "sources": sources
        }
    
    def clear_memory(self):
        """Clear conversation memory."""
        self.chat_history = []
