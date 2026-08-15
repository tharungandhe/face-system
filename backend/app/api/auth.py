from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form, Request
from app.services.registration_service import register_user
from app.services.authentication_service import authenticate_user
from app.services.jwt_service import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
async def register(
    username: str = Form(None),
    file: UploadFile = File(...),
    request: Request = None
):
    """
    Register a new user using face image.
    """

    # if `username` wasn't parsed (some clients), try reading the form manually
    if not username and request is not None:
        form = await request.form()
        username = form.get("username")

    result = await register_user(
        username=username,
        image=file
    )

    # create access token for new user so frontend can auto-login
    token = create_access_token({
        "sub": str(result["user_id"]),
        "username": result["username"]
    })

    return {
        "status": "success",
        "message": "User registered",
        "access_token": token,
        "token_type": "bearer",
        "data": result
    }


@router.post("/login")
async def login(
    file: UploadFile = File(...)
):
    """
    Login using face authentication.
    """

    user = await authenticate_user(file)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Face not recognized"
        )

    token = create_access_token(
        {
            "sub": str(user["user_id"]),
            "username": user.get("username")
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }