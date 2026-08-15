from app.services.embedding_service import EmbeddingService
from app.services.milvus_service import MilvusService
from app.database.user_mapping import save_username_mapping

embedding_service = EmbeddingService()
milvus_service = MilvusService()

class RegistrationService:

    async def register_user(self, username, image):
        """
        1. Extract embedding
        2. Store in vector DB
        """

        embedding = await embedding_service.extract(image)

        user_id = hash(username) % 10000

        milvus_service.insert_user(user_id, embedding)
        
        # Save mapping of user_id to username
        save_username_mapping(user_id, username)

        return {
            "user_id": user_id,
            "username": username
        }


# module-level helper for router imports
_registration_service = RegistrationService()

async def register_user(username, image):
    return await _registration_service.register_user(username, image)