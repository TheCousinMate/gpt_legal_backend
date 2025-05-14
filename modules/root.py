
from fastapi import APIRouter

router = APIRouter()

@router.get("/status/json")
def status_json():
    return {"status": "ok", "mensaje": "El backend está operativo y responde en JSON"}
