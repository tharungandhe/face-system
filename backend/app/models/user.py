from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    """
    User model for Face Authentication system
    """

    user_id: Optional[int] = None
    username: str
    email: Optional[str] = None
    is_active: bool = True