import sys
import os

# Ensure Python can find the backend module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.memory.neo4j_client import Neo4jClient

def test_memory():
    print("[SYSTEM] Testing Neo4j Memory Layer...")
    
    try:
        # Connect to Neo4j
        client = Neo4jClient()
        
        # 1. Log a test project
        project_id = "test-proj-001"
        print("-> Saving Project: Build a weather app")
        client.log_project(project_id, "Build a weather app")
        
        # 2. Log a decision
        print("-> Saving Decision: Use Python and Flask")
        client.log_decision(project_id, "Architect", "Chosen Python and Flask for rapid prototyping.")
        
        # 3. Retrieve decisions
        print("-> Retrieving Project Memory...")
        memory = client.get_project_decisions(project_id)
        
        for item in memory:
            print(f"   [Remembered] {item['agent']} decided: {item['rationale']}")
            
        client.close()
        print("\n[SUCCESS] Memory Layer Test Passed! The AI can now remember things.")
        
    except Exception as e:
        print(f"\n[ERROR] Error connecting to Neo4j: {e}")
        print("Make sure you have started Docker and run 'docker-compose up -d'")

if __name__ == "__main__":
    test_memory()
