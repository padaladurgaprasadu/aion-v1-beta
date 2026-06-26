import asyncio
from dotenv import load_dotenv
load_dotenv("backend/.env")

from backend.orchestrator.graph import build_generate_graph
from backend.orchestrator.state import AiONState

async def run_test():
    graph = build_generate_graph()
    
    initial_state = AiONState(
        goal="Build a simple Hello World React app",
        project_id="test_recheck_123",
        agent_role="Fullstack Web Developer",
        modules=["Frontend"],
        blueprint={
            "tech_stack": {"frontend": "React", "backend": "Node.js"},
            "file_structure": [
                "package.json",
                "server.js",
                "client/package.json",
                "client/src/App.js",
                "client/src/index.js"
            ]
        },
        code_files={},
        error=None,
        runtime_error=None,
        review_feedback=None,
        revision_count=0,
        execution_retries=0,
        execution_logs=[]
    )
    
    print("Starting generation test...")
    final_state = None
    for output in graph.stream(initial_state):
        node_name = list(output.keys())[0]
        final_state = output[node_name]
        print(f"--- Node Finished: {node_name} ---")
        if "runtime_error" in final_state and final_state["runtime_error"]:
            print(f"RUNTIME ERROR CAUGHT: {final_state['runtime_error']}")
        if "review_feedback" in final_state and final_state["review_feedback"]:
            print(f"REVIEW FEEDBACK: {final_state['review_feedback'][:100]}...")
            
    print("\n\nTest Finished!")
    if final_state and not final_state.get("runtime_error"):
        print("✅ SUCCESS: Project generated and passed execution!")
    else:
        print("❌ FAILED: Final state contains runtime error.")

if __name__ == "__main__":
    asyncio.run(run_test())
