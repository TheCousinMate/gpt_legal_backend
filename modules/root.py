# modules/root.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/")
def estado_backend():
    return JSONResponse(content={"estado": "vivo", "versión": "4.1.0"})
