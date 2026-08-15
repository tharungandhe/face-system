import jwt
import datetime
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.jwt_service import SECRET_KEY

ALGORITHM = "HS256"

security = HTTPBearer()

class Security:

    def create_token(self, user_id: int):
        """
        Generate JWT token
        """

        payload = {
            "sub": str(user_id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return token

    def verify_token(self, token: str):
        """
        Decode JWT token
        """

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded
        except:
            raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    FastAPI dependency for protected routes
    """

    token = credentials.credentials

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "user_id": decoded["sub"]
        }
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")