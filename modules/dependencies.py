from fastapi import Header, HTTPException
import os

# Lee desde .env
API_KEY_SECRET = os.getenv("API_KEY_SECRET")

async def verify_token(x_api_key: str = Header(...)):
    if x_api_key != API_KEY_SECRET:
        raise HTTPException(status_code=403, detail="Token inválido")
