@echo off
echo Activando entorno virtual...
call env\Scripts\activate

echo.
echo Agregando cambios al repositorio...
git add .
git commit -m "AutoPush 2025-05-14_16-33"
git push origin main

echo.
echo Iniciando servidor FastAPI con Uvicorn...
uvicorn main:app --reload --port 8000