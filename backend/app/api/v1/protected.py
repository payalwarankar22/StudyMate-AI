
from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/protected",
    tags=["Protected"]
)


@router.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return{
        "message": "You are authenticated",
        "user_id": current_user.id,
        "email": current_user.email
    }

            