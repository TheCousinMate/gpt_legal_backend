@echo off
echo Iniciando backend con Uvicorn...
start cmd /k "cd /d C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend && uvicorn main:app --reload"

echo Esperando 5 segundos para que el servidor se inicie...
timeout /t 5 >nul

echo Ejecutando tests robustos...
cd /d C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\tests
python test_all_endpoints_robusto.py

echo.
pause
