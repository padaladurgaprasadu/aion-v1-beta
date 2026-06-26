from backend.agents.base import BaseAgent
from langchain_core.messages import HumanMessage, SystemMessage
from backend.orchestrator.state import AiONState
import json

class AIMLModelTrainingAgent(BaseAgent):
    def __init__(self):
        super().__init__(temperature=0.2)
        
    def run(self, state: AiONState) -> dict:
        """Generates advanced ML training loops based on the blueprint and generated code."""
        
        # Only execute if the role is ML-related
        ml_roles = ["Machine Learning Engineer", "Data Scientist", "Deep Learning Researcher"]
        if state.get("agent_role") not in ml_roles:
            return {"code_files": state.get("code_files", {})}
            
        print("🤖 [AIML Trainer] Generating robust training loops and data loaders...")
        
        goal = state.get("goal")
        blueprint = state.get("blueprint", {})
        code_files = state.get("code_files", {})
        
        system_prompt = """You are the AiON AI/ML Model Training Agent.
Your job is to analyze the user's ML goal and the current codebase, and generate a highly robust `train.py` script.
The script MUST include:
1. Data loading and preprocessing.
2. The complete model training loop (PyTorch, TensorFlow, or Scikit-learn).
3. Loss functions and optimizers.
4. Evaluation metrics (Accuracy, F1, MSE, etc.).
5. Model saving/checkpointing logic.

Return ONLY a JSON object containing the new or updated files. Do NOT use markdown code blocks like ```json.
Format:
{
  "train.py": "import torch\\n..."
}"""

        prompt = f"""
Goal: {goal}
Blueprint: {json.dumps(blueprint, indent=2)}

Current Code Files:
{json.dumps(code_files, indent=2)}

Generate the robust training scripts and return the valid JSON object.
"""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            content = response.content
            if isinstance(content, list):
                content = "".join(c.get("text", "") if isinstance(c, dict) else str(c) for c in content)
            
            content = content.strip().strip('`').replace('json\n', '').strip()
            new_files = json.loads(content, strict=False)
            
            # Merge new files into existing code files
            merged_files = {**code_files, **new_files}
            return {"code_files": merged_files}
            
        except Exception as e:
            print(f"⚠️ [AIML Trainer] Failed to generate training logic: {e}")
            return {"code_files": code_files}
