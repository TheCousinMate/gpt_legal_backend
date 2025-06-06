from fastapi import Header, HTTPException

async def verify_token(x_api_key: str = Header(...)):
    if x_api_key != "tu_clave_secreta":
        raise HTTPException(status_code=403, detail="Token inválido")
