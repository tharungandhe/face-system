from fastapi import APIRouter, Depends
from app.utils.security import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.get("/profile")
async def profile(
    current_user: dict = Depends(get_current_user)
):
    """
    Get logged-in user profile.
    """

    return {
        "user_id": current_user["user_id"],
        "username": current_user.get("username", f"user_{current_user['user_id']}")
    }


@router.get("/dashboard")
async def dashboard(
    current_user: dict = Depends(get_current_user)
):
    """
    Protected dashboard.
    """

    return {
        "message": f"Welcome {current_user.get('username', f'user_{current_user["user_id"]}')}",
        "authenticated": True
    }