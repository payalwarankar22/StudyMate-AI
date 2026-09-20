

from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.protected import router as protected_router
from app.api.v1.notes import router as notes_router



router = APIRouter()

router.include_router(health_router)
router.include_router(auth_router)
router.include_router(protected_router)
router.include_router(notes_router)




