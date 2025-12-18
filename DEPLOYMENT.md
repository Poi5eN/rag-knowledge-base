# 🚀 Deployment Guide - RAG Knowledge Base

This guide will help you deploy your RAG Knowledge Base to **Streamlit Cloud** for FREE and get a shareable URL to showcase to YC recruiters.

## Prerequisites

✅ Completed application code
✅ Google API Key (free from [Google AI Studio](https://makersuite.google.com/app/apikey))
✅ GitHub account (free)
✅ Streamlit Cloud account (free)

---

## Step 1: Get Your Google API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **"Create API Key"**
3. Copy the API key - you'll need this later
4. Save it securely (you'll add it to Streamlit Cloud secrets)

> **Free Tier Limits**: 15 requests/minute, 1,500 requests/day - Perfect for demos!

---

## Step 2: Prepare Your Code for Deployment

### 2.1 Test Locally First

Add your API key to `.env`:

```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

Test the app:

```bash
# Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run the app
streamlit run app.py
```

Visit `http://localhost:8501` and test:

- Upload a PDF
- Ask questions
- Verify streaming responses work
- Check source citations

### 2.2 Create GitHub Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: RAG Knowledge Base with Gemini"

# Create a new repository on GitHub (https://github.com/new)
# Then push your code
git remote add origin https://github.com/YOUR_USERNAME/rag-knowledge-base.git
git branch -M main
git push -u origin main
```

---

## Step 3: Deploy to Streamlit Cloud

### 3.1 Sign Up for Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Authorize Streamlit to access your repositories

### 3.2 Deploy Your App

1. Click **"New app"**
2. Select your repository: `your-username/rag-knowledge-base`
3. Set the main file: `app.py`
4. Click **"Advanced settings"**
5. Set Python version: `3.11` (recommended)

### 3.3 Add Secrets (Important!)

In the **Advanced settings**, under **Secrets**, add:

```toml
GOOGLE_API_KEY = "your_actual_google_api_key_here"
```

> **Note**: Replace `your_actual_google_api_key_here` with your real API key (keep the quotes)

### 3.4 Deploy!

1. Click **"Deploy!"**
2. Wait 2-5 minutes for deployment
3. Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

---

## Step 4: Test Your Deployed App

1. Visit your app URL
2. Upload a sample PDF (try a research paper or documentation)
3. Ask questions about the document
4. Verify:
   - ✅ PDF uploads successfully
   - ✅ Processing completes without errors
   - ✅ Chat responses are streamed
   - ✅ Source citations appear
   - ✅ UI looks beautiful

---

## Step 5: Customize Your Deployment

### Update App Name

1. In Streamlit Cloud dashboard, click your app
2. Click **Settings** → **General**
3. Update **App name** to something professional like:
   - `rag-knowledge-base`
   - `ai-document-chat`
   - `smart-pdf-assistant`

Your URL will become: `https://your-app-name.streamlit.app`

### Add a Custom Domain (Optional)

If you have a domain, you can connect it in Settings → Custom domain

---

## Step 6: Share With Recruiters

### Create a Landing Description

Update your GitHub README and add:

**Live Demo**: [https://your-app-name.streamlit.app](https://your-app-name.streamlit.app)

### What to Highlight

When sharing with YC recruiters, emphasize:

1. **Production-Ready RAG System**

   - Vector database integration
   - Semantic search with embeddings
   - Streaming LLM responses

2. **Modern AI Stack**

   - Google Gemini API integration
   - LangChain framework
   - ChromaDB vector store
   - Sentence Transformers

3. **Full-Stack Development**

   - Backend: Python, async processing
   - Frontend: Modern UI with Streamlit
   - Deployment: Cloud infrastructure

4. **Best Practices**
   - Git version control
   - Environment variable management
   - Error handling
   - Resource caching
   - Responsive design

---

## Troubleshooting

### Issue: "GOOGLE_API_KEY not found"

**Solution**: Make sure you added the API key in Streamlit Cloud secrets (Step 3.3)

### Issue: App crashes during PDF processing

**Solution**: Check Streamlit Cloud logs in the hamburger menu → Manage app → Logs

### Issue: Slow responses

**Solution**: This is normal for free tier. Google Gemini free tier may have rate limits.

### Issue: Module not found errors

**Solution**: Ensure all dependencies are in `requirements.txt` and properly formatted

---

## Performance Tips

1. **Use smaller PDFs for demo** (< 20 pages work best)
2. **Clear chat history** if responses slow down
3. **Keep questions concise** for faster responses
4. **Upload 1-3 documents max** for optimal demo experience

---

## Updating Your Deployed App

Any changes pushed to your GitHub main branch will automatically redeploy:

```bash
# Make changes to your code
git add .
git commit -m "Update: improved UI"
git push origin main

# Streamlit Cloud will auto-deploy (2-3 minutes)
```

---

## Cost Breakdown (All FREE!)

| Service             | Cost         | What You Get                            |
| ------------------- | ------------ | --------------------------------------- |
| **Streamlit Cloud** | $0           | Hosting, 1GB resources, auto-deployment |
| **Google Gemini**   | $0           | 1,500 requests/day, streaming responses |
| **ChromaDB**        | $0           | Local storage, unlimited documents\*    |
| **GitHub**          | $0           | Code hosting, version control           |
| **Total**           | **$0/month** | Full production app!                    |

\* _Limited by Streamlit Cloud's 1GB storage - enough for hundreds of PDFs_

---

## Next Steps

1. ✅ Add screenshots to your README
2. ✅ Create a demo video showing the app in action
3. ✅ Add to your portfolio website
4. ✅ Link in your LinkedIn/resume
5. ✅ Share with YC recruiters!

---

## Example Email to Recruiters

```
Subject: AI Engineer Portfolio - RAG Knowledge Base Demo

Hi [Recruiter Name],

I've built a production-ready RAG (Retrieval-Augmented Generation) system
that showcases modern AI engineering skills.

🔗 Live Demo: https://your-app-name.streamlit.app
📦 Source Code: https://github.com/your-username/rag-knowledge-base

Key Features:
- Google Gemini LLM integration with streaming responses
- Vector search using ChromaDB and Sentence Transformers
- LangChain RAG pipeline with conversation memory
- Production-ready deployment on Streamlit Cloud

Tech Stack: Python, Streamlit, LangChain, Google Gemini, ChromaDB,
Sentence Transformers

Feel free to upload any PDF and ask questions - the AI will provide
accurate answers with source citations!

Best regards,
[Your Name]
```

---

**🎉 Congratulations!** Your RAG Knowledge Base is now live and ready to impress YC recruiters!

For support, check the [Streamlit Community](https://discuss.streamlit.io/) or [GitHub Issues](https://github.com/your-username/rag-knowledge-base/issues).
