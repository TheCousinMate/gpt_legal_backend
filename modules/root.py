# modules/root.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/")
def healthcheck():
    """Return service status and version."""
    return {"status": "alive", "version": "4.1.0"}
