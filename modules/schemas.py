from pydantic import BaseModel

class Mensaje(BaseModel):
    contenido: str

class PrediccionRequest(BaseModel):
    texto: str
    contexto: str = None

class PrediccionResponse(BaseModel):
    resultado: str
    confianza: float
