import os

class Settings:
    """
    App configuration settings
    """

    PROJECT_NAME = "Face Auth System"
    VERSION = "1.0.0"

    # JWT settings
    SECRET_KEY = "face-auth-secret"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS = 2

    # Milvus config
    MILVUS_HOST = "localhost"
    MILVUS_PORT = "19530"

    # Face embedding dimension
    EMBEDDING_DIM = 512

    # Upload settings
    UPLOAD_DIR = "uploads"

settings = Settings()