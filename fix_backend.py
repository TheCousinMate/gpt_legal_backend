import os
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
MODULES = ROOT / "modules"

# 1. Eliminar duplicado config_map.py en raíz
config_map_root = ROOT / "config_map.py"
config_map_module = MODULES / "config_map.py"

if config_map_root.exists() and config_map_module.exists():
    print("🗑️ Eliminando config_map.py duplicado del raíz")
    config_map_root.unlink()

# 2. Reescribir validacion_schema.py para quitar código de activación
validacion_path = MODULES / "validacion_schema.py"
print("✏️ Reescribiendo validacion_schema.py sin código de activación...")
validacion_code = '''
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from jsonschema import validate, ValidationError
import json
import os

router = APIRouter()

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "derecho_chileno_schema.json")

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    SCHEMA = json.load(f)

@router.post("/validar")
async def validar_entrada(request: Request):
    payload = await request.json()

    contenido = payload.get("contenido")
    if not contenido:
        raise HTTPException(status_code=400, detail="El campo 'contenido' es obligatorio.")

    try:
        validate(instance=contenido, schema=SCHEMA)
        return {
            "valido": True,
            "mensaje": "JSON válido según el esquema oficial.",
            "error": None
        }
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content={
                "valido": False,
                "mensaje": "JSON inválido.",
                "error": e.message
            }
        )
'''.strip()
validacion_path.write_text(validacion_code, encoding="utf-8")

# 3. Eliminar carpetas innecesarias como __pycache__
for cache in ROOT.rglob("__pycache__"):
    print(f"🧹 Eliminando carpeta {cache}")
    shutil.rmtree(cache)

# 4. Mover schema al módulo si quieres centralizarlo
# schema_src = ROOT / "schema_gpt_custom_derecho_chileno.json"
# schema_dst = MODULES / "derecho_chileno_schema.json"
# if schema_src.exists():
#     print("📦 Moviendo schema al módulo...")
#     shutil.move(str(schema_src), str(schema_dst))

print("✅ Limpieza y corrección completa.")
