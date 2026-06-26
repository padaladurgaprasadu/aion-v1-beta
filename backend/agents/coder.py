import re
import json
import concurrent.futures
from langchain_core.prompts import ChatPromptTemplate
from backend.agents.base import BaseAgent
from backend.orchestrator.state import AiONState

class CoderAgent(BaseAgent):
    """
    The Coder Agent generates code for multiple files simultaneously using multithreading.
    """
    def __init__(self):
        super().__init__()

    def _generate_single_file(self, blueprint_str, feedback, runtime_error, target_file, agent_role):
        
        # Dynamically adapt rules based on agent_role
        if "Research" in agent_role:
            framework_rules = "3. RESEARCH RULE: Write an extensive, academic, and highly detailed document for the requested file. Ensure you provide a NOVEL APPROACH with innovative ideas, avoiding generic statements. Use Markdown formatting. Do not write software code unless explicitly requested.\n4. Cite hypothetical but realistic methods where appropriate."
        elif "Fullstack" in agent_role or "Web" in agent_role or "UI" in agent_role:
            framework_rules = "3. CRITICAL PORT RULE: Your Express backend MUST run on PORT 5000. Your Vite React frontend will run on its default port, but you must configure your backend cors to accept requests.\n4. CRITICAL FRAMEWORK RULE: Write modular, clean code using React for the frontend and Node.js/Express for the backend. Use Tailwind CSS classes for styling.\n5. CRITICAL ROUTING RULE: You MUST use React Router v6 syntax. Do NOT use '<Switch>'. You MUST use '<Routes>' and '<Route path=\"/\" element={{<Component />}} />'.\n6. CRITICAL COMPONENT RULE: You MUST NOT import any components, contexts, or stores that you did not explicitly generate. If it's not in the blueprint's file_structure, DO NOT IMPORT IT.\n7. POSTGRESQL RULE: If using PostgreSQL, strictly use the connection string 'postgresql://postgres:postgres@localhost:5432/postgres'.\n8. CRITICAL BACKEND DEPENDENCY RULE: Your root 'package.json' MUST include 'express', 'cors', 'pg', 'dotenv', 'concurrently' and any other backend libraries. Its dev script MUST be: '\"dev\": \"concurrently \\\"node server.js\\\" \\\"cd client && npm run dev\\\"\"'.\n9. CRITICAL VITE RULE: The frontend is pre-scaffolded with Vite. You MUST NOT generate 'client/package.json', 'index.html', or 'main.jsx'. You ONLY generate 'client/src/App.jsx' and your custom components (e.g. 'client/src/components/Dashboard.jsx'). Every React file MUST end with '.jsx'."
        else:
            framework_rules = "3. CRITICAL PORT RULE: The app must run on port 3000 for the iframe preview.\n4. CRITICAL FRAMEWORK RULE: Write modular, clean code using the appropriate Python libraries for ML/Data Science (e.g. Pandas, Scikit-learn, PyTorch, Streamlit, FastAPI). Ensure all dependencies are documented in requirements.txt.\n5. Do NOT write React code unless explicitly requested in the blueprint. Use Streamlit for simple UIs.\n6. POSTGRESQL RULE: If using PostgreSQL, you MUST strictly use the connection string 'postgresql://postgres:postgres@localhost:5432/postgres'. Do NOT use environment variables for DB connections."

        system_prompt = f"You are a Senior AI {agent_role}. Given a blueprint, write the FULL production-grade content for the requested file: {{target_file}}.\n\nIMPORTANT RULES:\n1. Output the file EXACTLY in this format:\n\n<file path=\"{{target_file}}\">\n[YOUR CODE/CONTENT HERE]\n</file>\n\n2. Do NOT use JSON. Do not use markdown backticks outside of the file tags.\n{framework_rules}\n10. If you receive Review Feedback or a Runtime Error, you must fix the issues mentioned."

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Blueprint: {blueprint}\nTarget File: {target_file}\nReview Feedback: {review_feedback}\nRuntime Error: {runtime_error}")
        ])
        chain = prompt | self.llm
        
        import time
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                response = chain.invoke({
                    "blueprint": blueprint_str,
                    "target_file": target_file,
                    "review_feedback": feedback,
                    "runtime_error": runtime_error
                })
                content = response.content
                if isinstance(content, list):
                    content = "".join(c.get("text", "") if isinstance(c, dict) else str(c) for c in content)
                    
                import re
                match = re.search(r'<file\s+path="[^"]+">(.*?)</file>', content, re.DOTALL)
                if match:
                    code = match.group(1).strip()
                    print(f"   -> [Success] Generated {target_file}")
                    return (target_file, code)
                else:
                    print(f"   -> [Attempt {attempt+1}] Failed to parse XML tags for {target_file}.")
                    return target_file, f"// Error: AiON LLM failed to format {target_file} correctly"
                    
            except Exception as e:
                error_str = str(e)
                if "429" in error_str and attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 3
                    print(f"      - [WARNING] Rate limit hit for {target_file}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"      - [ERROR] Exception while generating {target_file}: {e}")
                    return target_file, f"// Error: AiON encountered an exception: {e}"

    def run(self, state: AiONState) -> AiONState:
        # If we already have code files (e.g. from Reviewer loop), we might only regenerate the ones with issues.
        # For simplicity, we just regenerate all or use the target files.
        files_to_generate = state["blueprint"].get("file_structure", ["src/server.js", "package.json"])
        
        print(f"[Coder] Generating {len(files_to_generate)} files in parallel...")
        
        blueprint_str = json.dumps(state["blueprint"])
        feedback = state.get("review_feedback", "None")
        runtime_error = state.get("runtime_error", "None")
        
        code_files = {}
        
        agent_role = state.get("agent_role", "Fullstack Web Developer")
        
        # Increment revision count if we are looping
        if feedback != "None" or runtime_error != "None":
            state["revision_count"] = state.get("revision_count", 0) + 1
            if runtime_error != "None":
                print(f"[Coder] Auto-Heal Triggered! Attempting to fix runtime error...")
        
        # Use ThreadPoolExecutor to run LLM calls in parallel
        # OpenRouter supports concurrent requests, so we can generate files much faster!
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(self._generate_single_file, blueprint_str, feedback, runtime_error, f, agent_role)
                for f in files_to_generate
            ]
            
            for future in concurrent.futures.as_completed(futures):
                path, file_content = future.result()
                code_files[path] = file_content
                
        state["code_files"] = code_files
        return state
