from fastapi import HTTPException

class InvalidLegalDocument(HTTPException):
    def __init__(self, detail="Documento legal inválido o corrupto"):
        super().__init__(status_code=422, detail=detail)

class PredictionModelError(HTTPException):
    def __init__(self, detail="Error en la predicción del modelo"):
        super().__init__(status_code=500, detail=detail)
