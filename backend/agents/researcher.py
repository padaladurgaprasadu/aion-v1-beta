import json
from backend.agents.base import BaseAgent
from backend.orchestrator.state import AiONState
from langchain_core.prompts import ChatPromptTemplate
from duckduckgo_search import DDGS

class ResearchAgent(BaseAgent):
    """
    The Research Agent is responsible for executing real-time web searches to gather
    the latest documentation, best practices, and API references before the Architect designs the system.
    This prevents hallucinations on cutting-edge frameworks (like Next.js App Router, latest Tailwind).
    """
    def __init__(self):
        super().__init__()
        # We use a fast model for query generation
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an elite AI Research Assistant. Your job is to read the user's project goal and determine the TOP 3 most important search queries needed to gather the latest documentation or best practices for this project. Output EXACTLY a JSON list of strings and nothing else. Example: [\"Next.js 15 app router best practices\", \"Tailwind CSS v4 components\", \"Stripe integration tutorial\"]"),
            ("human", "Goal: {goal}\nTech Role: {agent_role}")
        ])
        self.chain = self.prompt | self.llm

    def run(self, state: AiONState) -> AiONState:
        goal = state.get("goal", "")
        agent_role = state.get("agent_role", "")
        
        print(f"[ResearchAgent] Planning research strategy for: {goal}")
        
        try:
            # 1. Ask LLM for the best search queries
            response = self.chain.invoke({
                "goal": goal,
                "agent_role": agent_role
            })
            
            content = response.content
            # Clean up potential markdown formatting
            content = content.replace("```json", "").replace("```", "").strip()
            queries = json.loads(content)
            
            if not isinstance(queries, list):
                queries = [goal]
                
        except Exception as e:
            print(f"   -> [ResearchAgent] Error generating queries: {e}. Falling back to default search.")
            queries = [goal + " " + agent_role + " best practices"]
            
        # Limit to 3 queries to save time
        queries = queries[:3]
        
        gathered_context = ""
        ddgs = DDGS()
        
        # 2. Execute Web Search
        for query in queries:
            print(f"   -> [ResearchAgent] Searching web: '{query}'...")
            try:
                # Get top 3 text results per query
                results = ddgs.text(query, max_results=3)
                for res in results:
                    gathered_context += f"Source: {res.get('title', 'Unknown')}\nURL: {res.get('href', 'N/A')}\nSnippet: {res.get('body', '')}\n\n"
            except Exception as e:
                print(f"      - Search failed for '{query}': {e}")
                
        if gathered_context:
            print(f"   -> [ResearchAgent] Successfully gathered {len(gathered_context)} bytes of real-time web context.")
            
            # 3. Append to semantic context so the Architect and Coder can read it
            existing_context = state.get("semantic_context", "")
            new_context = existing_context + "\n\n=== LATEST WEB RESEARCH ===\n" + gathered_context
            state["semantic_context"] = new_context
        else:
            print("   -> [ResearchAgent] No relevant web context found.")

        return state
