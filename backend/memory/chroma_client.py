import chromadb
from chromadb.utils import embedding_functions

class ChromaClient:
    """
    Manages the Vector Database (ChromaDB) for Semantic Memory.
    It stores projects and their architectures so the AI can search for them by 'meaning'.
    """
    def __init__(self, db_path="./chroma_db"):
        # Initialize a local ChromaDB instance
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Use ChromaDB's default local sentence-transformer model for embeddings
        # This runs 100% locally and does not require an API key!
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        # Get or create our 'blueprints' collection
        self.collection = self.client.get_or_create_collection(
            name="blueprints",
            embedding_function=self.embedding_fn
        )

    def store_blueprint(self, project_id, goal, blueprint):
        """Stores the project's goal and resulting blueprint into the vector database."""
        # We embed the 'goal' so we can search by goal later
        document = f"Goal: {goal}\nBlueprint: {blueprint}"
        
        # We use upsert so it overwrites if it already exists
        self.collection.upsert(
            documents=[document],
            metadatas=[{"project_id": project_id, "goal": goal}],
            ids=[project_id]
        )

    def find_similar_projects(self, new_goal, n_results=2):
        """Searches the database for past projects similar to the new goal."""
        try:
            # Check how many items are in the DB so we don't request more than exists
            count = self.collection.count()
            if count == 0:
                return []
                
            n = min(n_results, count)
            
            results = self.collection.query(
                query_texts=[new_goal],
                n_results=n
            )
            
            # Extract and return the documents if any exist
            if results and results["documents"] and len(results["documents"][0]) > 0:
                return results["documents"][0]
            return []
        except Exception as e:
            print(f"   -> [WARNING] ChromaDB search failed: {e}")
            return []
