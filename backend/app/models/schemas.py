from pydantic import BaseModel
from typing import Optional

# =========================
# Register Request Schema
# =========================
class RegisterRequest(BaseModel):
    username: str


# =========================
# Login Response Schema
# =========================
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# =========================
# User Profile Response
# =========================
class UserProfile(BaseModel):
    user_id: int
    username: str
    email: Optional[str] = None


# =========================
# Face Match Response
# =========================
class FaceMatchResponse(BaseModel):
    user_id: int
    username: str
    score: float