from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ProxyInput(BaseModel):
    input: str

@router.post("/")
def analizarProxy(data: ProxyInput):
    # Lógica proxy aquí
    return {"resultado": f"Resultado del proxy sobre: {data.input}"}
