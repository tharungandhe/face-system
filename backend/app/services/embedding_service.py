from app.services.facenet_service import FaceNetService

facenet = FaceNetService()


class EmbeddingService:

    async def extract(self, image):
        """
        Return face embedding vector (async)
        """
        return await facenet.get_embedding(image)