from fastapi import APIRouter

router = APIRouter()

@router.get("/json")
def estadoBackend():
    # Estado actual backend
    return {
        "status": "operativo",
        "endpoints": 7
    }
