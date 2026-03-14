from fastapi import APIRouter
from app.database import check_db

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/live")
def live():
    return {"status": "alive"}

@router.get("/startup")
def startup():
    return {"status": "started"}

@router.get("/ready")
def ready():

    if not check_db():
        return {"status": "not ready"}

    return {"status": "ready"}
