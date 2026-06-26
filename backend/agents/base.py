import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from the .env file
load_dotenv()

class BaseAgent:
    """
    A base class that sets up the AI model (LLM) so all other agents can inherit it.
    """
    def __init__(self, model_name="google/gemini-2.5-flash", temperature=0.2):
        self.model_name = model_name
        self.temperature = temperature
        
        # Load from .env natively
        groq_keys_str = os.getenv("GROQ_API_KEYS") or os.getenv("GROQ_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        ollama_model = os.getenv("OLLAMA_MODEL")
        nvidia_key = os.getenv("NVIDIA_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        import random
        
        if openai_key:
            print("[DEBUG] Using Native OpenAI Endpoint (gpt-4o)")
            self.llm = ChatOpenAI(
                api_key=openai_key.strip(),
                model="gpt-4o",
                temperature=self.temperature,
                max_tokens=4000
            )
        elif nvidia_key:
            print("[DEBUG] Using NVIDIA NIM Endpoint (Llama 3.1 70B)")
            self.llm = ChatOpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=nvidia_key.strip(),
                model="meta/llama-3.1-70b-instruct",
                temperature=self.temperature,
                max_tokens=4000
            )
        elif ollama_model:
            print(f"[DEBUG] Using Local Ollama with model: {ollama_model}")
            self.llm = ChatOpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",
                model=ollama_model,
                temperature=self.temperature,
                max_tokens=4000
            )
        elif groq_keys_str:
            keys = [k.strip() for k in groq_keys_str.split(',') if k.strip()]
            chosen_key = random.choice(keys) if keys else "dummy"
            print(f"[DEBUG] Using Groq (Llama 3.3) with key ...{chosen_key[-4:]}")
            
            self.llm = ChatOpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=chosen_key,
                model="llama-3.3-70b-versatile",
                temperature=self.temperature,
                max_tokens=4000
            )
        elif gemini_key:
            print("[DEBUG] Using Native Google Gemini SDK")
            native_model = "gemini-2.0-flash"
                
            self.llm = ChatGoogleGenerativeAI(
                model=native_model,
                google_api_key=gemini_key.strip(),
                temperature=self.temperature,
                max_tokens=4000
            )
        elif openrouter_key:
            print("[DEBUG] Using Premium OpenRouter (Claude 3.5 Sonnet)")
            self.llm = ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=openrouter_key.strip(),
                model="anthropic/claude-3.5-sonnet",
                temperature=self.temperature,
                max_tokens=4000
            )
        else:
            print("[DEBUG] Using OpenRouter (Free Tier)")
            self.llm = ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=openrouter_key or "dummy_key",
                model="google/gemini-2.0-flash-lite-preview-02-05:free",
                temperature=self.temperature,
                max_tokens=3000
            )
