import jwt
import datetime

SECRET_KEY = "supersecretkey"

class JWTService:

    def create_token(self, data: dict):
        """
        Generate JWT token
        """

        payload = data.copy()
        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=2)

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return token

    def verify_token(self, token: str):
        """
        Decode JWT token
        """
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return decoded
        except:
            return None


# module-level helpers for router imports
_jwt_service = JWTService()

def create_access_token(data: dict):
    return _jwt_service.create_token(data)

def verify_access_token(token: str):
    return _jwt_service.verify_token(token)