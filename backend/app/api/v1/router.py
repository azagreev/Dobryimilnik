from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.domains.imports.api import router as imports_router

router = APIRouter()
router.include_router(health_router)
router.include_router(imports_router, prefix="/imports", tags=["imports"])
