from pydantic import BaseModel, Field
import json
from langchain_core.messages import HumanMessage, SystemMessage
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
Analyze the user's message and extract exactly four dimensions.

RULES:
1. Output ONLY a valid JSON object in this format:
{
  "domain": "e.g., Education, Software Engineering, Travel, Medicine, Finance",
  "specific_intent": "MUST BE EXACTLY ONE OF: Definition, Tutorial, Comparison, Roadmap, Code Generation, Debugging, Project, System Architecture",
  "complexity": "Beginner, Intermediate, or Advanced",
  "style": "e.g., Step-by-step phases, Clear and concise, Q&A format, Table comparison",
  "avoid_sections": ["list", "of", "sections", "or", "elements", "to", "strictly", "avoid"]
}
2. Do NOT output any other text, markdown, or explanation.
"""

    def detect_intent(self, message: str, history: list = None) -> dict:
        """
        Runs a fast LLM inference to determine the user's multi-dimensional intent.
        """
        try:
            context = f"User Message: {message}"
            if history and len(history) > 0:
                context = f"Previous context: {history[-1].get('content', '')[:100]}\n{context}"

            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=context)
            ]
            
            response = self.llm.invoke(messages)
            content = response.content.strip()
            
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
                
            data = json.loads(content)
            logger.info(f"[ROUTER] Detected Intent: {data}")
            return data
            
        except Exception as e:
            logger.warning(f"[ROUTER] Intent detection failed, falling back to GENERAL. Error: {e}")
            return {
                "domain": "General",
                "specific_intent": "General Chat",
                "complexity": "Intermediate",
                "style": "Clear and concise"
            }
