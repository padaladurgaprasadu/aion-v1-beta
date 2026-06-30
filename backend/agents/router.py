from pydantic import BaseModel, Field
import json
from langchain_core.messages import HumanMessage, SystemMessage
from backend.agents.prompts import IntentCategory
from backend.utils.logger import get_logger

logger = get_logger("AiON_Router")

class IntentRouter:
    def __init__(self, llm):
        """
        Initializes the IntentRouter with an LLM. 
        For speed, we should ideally use a fast model (e.g., Llama 3 8B), but we accept the system default.
        """
        self.llm = llm
        
        self.system_prompt = """
You are an ultra-fast Intent Detection Engine.
Analyze the user's message and categorize it into EXACTLY ONE of the following categories:
LEARNING, CODING, DEBUGGING, RESEARCH, TRAVEL, SHOPPING, MEDICAL, FINANCE, LEGAL, WRITING, TRANSLATION, BRAINSTORMING, PROJECT_PLANNING, CAREER, GENERAL.

RULES:
1. Output ONLY a valid JSON object in this format: {"intent": "CATEGORY"}
2. Do NOT output any other text, markdown, or explanation.
3. If unsure, fallback to "GENERAL".
"""

    def detect_intent(self, message: str, history: list = None) -> IntentCategory:
        """
        Runs a fast LLM inference to determine the user's intent.
        """
        try:
            # Prepare context. If it's a follow-up, the history helps contextualize.
            # But we keep it short to save TTFT.
            context = f"User Message: {message}"
            if history and len(history) > 0:
                context = f"Previous context: {history[-1].get('content', '')[:100]}\n{context}"

            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=context)
            ]
            
            # We don't stream this, we just invoke it.
            # Some Langchain models support structured output, but for maximum compatibility across OpenAI, Groq, NVIDIA, Ollama:
            # We just parse the raw string.
            response = self.llm.invoke(messages)
            content = response.content.strip()
            
            # Strip markdown if the LLM ignored Rule 2
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
                
            data = json.loads(content)
            intent_str = data.get("intent", "GENERAL").upper()
            
            # Safely cast to Enum
            try:
                intent = IntentCategory(intent_str)
            except ValueError:
                intent = IntentCategory.GENERAL
                
            logger.info(f"[ROUTER] Detected Intent: {intent.value}")
            return intent
            
        except Exception as e:
            logger.warning(f"[ROUTER] Intent detection failed, falling back to GENERAL. Error: {e}")
            return IntentCategory.GENERAL
