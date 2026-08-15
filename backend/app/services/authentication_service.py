from app.services.embedding_service import EmbeddingService
from app.services.milvus_service import MilvusService
from app.database.user_mapping import get_username_from_id

embedding_service = EmbeddingService()
milvus_service = MilvusService()

class AuthenticationService:

    async def authenticate_user(self, image):
        """
        1. Extract embedding
        2. Search in vector DB
        3. Return best match
        """

        embedding = await embedding_service.extract(image)

        result = milvus_service.search_face(embedding)

        try:
            print(f"[AuthenticationService] search result={result}")
            import sys
            sys.stdout.flush()
        except Exception:
            pass

        # milvus_client.search returns a distance (lower is better) for in-memory fallback,
        # so treat a small distance as a match. Return None if no result.
        if result and result.get("score") is not None:
            # OpenCV SFace L2 distance threshold is ~1.128. We'll use 1.25 for slight leniency.
            if result["score"] < 1.25:
                mapped_name = get_username_from_id(result["id"])
                username = mapped_name if mapped_name else "user_" + str(result["id"])
                return {
                    "user_id": result["id"],
                    "score": result["score"],
                    "username": username
                }

        return None


# module-level helper for router imports
_authentication_service = AuthenticationService()

async def authenticate_user(image):
    return await _authentication_service.authenticate_user(image)