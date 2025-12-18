# 🧠 RAG Knowledge Base

A production-ready Retrieval-Augmented Generation (RAG) system that allows users to upload PDFs and chat with them using AI. Built with 100% free and open-source technologies.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.29+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 📄 **PDF Upload**: Upload and process multiple PDF documents
- 💬 **AI Chat Interface**: Ask questions and get intelligent answers
- 🔍 **Vector Search**: Semantic search using ChromaDB
- 📚 **Source Citations**: See which documents answers come from
- ⚡ **Streaming Responses**: Real-time AI responses with typewriter effect
- 🎨 **Modern UI**: Beautiful glassmorphism design with dark theme
- 🆓 **100% Free**: Uses free tiers and open-source models

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: Google Gemini 1.5 Flash (Free Tier)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB (Local)
- **Framework**: LangChain
- **PDF Processing**: PyPDF2

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Google API Key (free from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or download the project**:

   ```bash
   cd rag-knowledge-base
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   - Copy `.env.example` to `.env`
   - Add your Google API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

5. **Run the application**:

   ```bash
   streamlit run app.py
   ```

6. **Open your browser** to `http://localhost:8501`

## 📖 Usage

1. **Upload PDFs**: Click the upload button and select your PDF files
2. **Process Documents**: Click "Process Documents" to analyze your PDFs
3. **Start Chatting**: Ask questions about your documents in the chat interface
4. **View Sources**: Expand source citations to see where answers came from
5. **Manage Documents**: Use the sidebar to view and delete documents

## 🏗️ Project Structure

```
rag-knowledge-base/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
├── src/
│   ├── components/
│   │   ├── chat_interface.py       # Chat UI component
│   │   ├── pdf_uploader.py         # PDF upload component
│   │   └── sidebar.py              # Sidebar component
│   ├── core/
│   │   ├── embeddings.py           # Embedding generation
│   │   ├── pdf_processor.py        # PDF processing
│   │   ├── rag_pipeline.py         # RAG logic
│   │   └── vector_store.py         # ChromaDB integration
│   └── utils/
│       ├── config.py               # Configuration
│       └── session_state.py        # State management
└── assets/
    └── styles.py                   # Custom CSS styles
```

## 🎨 UI Features

- **Glassmorphism Effects**: Modern semi-transparent UI elements
- **Smooth Animations**: Fade-ins, hover effects, and transitions
- **Gradient Accents**: Beautiful color gradients throughout
- **Dark Theme**: Professional dark mode with proper contrast
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🚀 Deployment

### Deploy to Streamlit Cloud (Free)

1. **Push to GitHub**:

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your-repo-url
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:

   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `app.py` as the main file
   - Add `GOOGLE_API_KEY` in Secrets Management
   - Click Deploy!

3. **Share your URL** with recruiters!

## 🔑 Getting API Keys

### Google Gemini API (Free)

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy and paste into your `.env` file

**Free Tier Limits**:

- 15 requests per minute
- 1,500 requests per day
- Perfect for demos and personal projects!

## 💡 Tips for YC Recruiters

This project demonstrates:

- ✅ **Modern AI Engineering**: RAG, vector databases, LLM integration
- ✅ **Production-Ready Code**: Clean architecture, error handling, caching
- ✅ **UX Excellence**: Streaming responses, source citations, beautiful UI
- ✅ **Full-Stack Skills**: Frontend (Streamlit), backend (Python), AI/ML
- ✅ **Deployment**: Cloud-ready with free hosting

## 🤝 Contributing

Feel free to fork, improve, and submit pull requests!

## 📝 License

MIT License - feel free to use this project for your portfolio!

## 🌟 Showcase

Add screenshots or a demo video here after deployment!

---

**Built with ❤️ for YC Recruiters**

_Powered by Google Gemini, ChromaDB, and LangChain_
