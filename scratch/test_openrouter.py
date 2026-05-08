import os
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_openai import ChatOpenAI

load_dotenv()

def test_openrouter():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found in .env")
        return

    print(f"Testing OpenRouter with key: {api_key[:10]}...")
    
    try:
        llm = ChatOpenAI(
            model="openrouter/auto",
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "https://github.com/rag-knowledge-base",
                "X-Title": "RAG Knowledge Base Test"
            }
        )
        
        response = llm.invoke("Say hello and tell me what model you are.")
        print("\nResponse from OpenRouter:")
        print(response.content)
        print("\nOpenRouter API key is WORKING!")
        
    except Exception as e:
        print(f"\nError testing OpenRouter: {str(e)}")

if __name__ == "__main__":
    test_openrouter()
