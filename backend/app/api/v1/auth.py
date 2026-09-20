
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.schemas.auth import RegisterRequest, LoginRequest
from app.services.auth_service import AuthService
from app.database.database import get_db

from app.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


#####################################################################

# Register Router
@router.post("/register")
def register(
    request:RegisterRequest, 
    db: Session = Depends(get_db)
    ):
    
    service = AuthService()

    return service.register_user(
        db=db,
        name=request.name, 
        email=request.email,
        password= request.password
    )


#################################################################################

#Login Route
@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
    ):

    service = AuthService()

    return service.login_user(
        db = db,
        email=request.email,
        password=request.password
    )


#######################################################################################
# protected /me route

@router.get("/me")
def get_me(
    current_user = Depends(get_current_user)
):
    return {
        "id" : current_user.id,
        "name" : current_user.name,
        "email" : current_user.email

    }


