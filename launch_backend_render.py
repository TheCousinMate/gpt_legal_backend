# launch_backend_render.py
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render lo asigna, 10000 por defecto
    print(f"🚀 Iniciando servidor en el puerto {port}...")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
