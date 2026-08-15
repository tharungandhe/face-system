from app.database.milvus_client import MilvusClient

# Use a shared client instance so fallback in-memory embeddings persist across
# registration and login when Milvus itself is unavailable.
_shared_milvus_client = MilvusClient()

class MilvusService:
    def __init__(self):
        self.db = _shared_milvus_client

    def insert_user(self, user_id, embedding):
        """
        Store embedding in vector DB
        """
        # MilvusClient.insert expects a list of items
        self.db.insert([
            {
                "id": user_id,
                "vector": embedding
            }
        ])

        return True

    def search_face(self, embedding):
        """
        Find closest match
        """
        result = self.db.search(embedding)
        try:
            print(f"[MilvusService] search result={result}")
        except Exception:
            pass

        return result