# Paso 1: Ir al directorio del proyecto
cd "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend"

# Paso 2: Eliminar el antiguo archivo openapi.yaml si existe
if (Test-Path ".\openapi.yaml") {
    Remove-Item ".\openapi.yaml" -Force
    Write-Host "✅ Archivo antiguo 'openapi.yaml' eliminado"
}

# Paso 3: Renombrar correctamente el archivo nuevo
Rename-Item "openapi_with_text_search.yaml" "openapi.yaml"
Write-Host "✅ Archivo renombrado a 'openapi.yaml'"

# Paso 4: Confirmar que el archivo existe
if (Test-Path ".\openapi.yaml") {
    Write-Host "✅ Confirmado: 'openapi.yaml' listo en la raíz del proyecto"
} else {
    Write-Host "❌ Error: 'openapi.yaml' no se encontró"
    exit 1
}

# Paso 5: Agregar a git, commitear y pushear
git add openapi.yaml
git commit -m "chore: renombrado y agregado openapi.yaml con definición actualizada"
git push origin main
Write-Host "✅ Git actualizado y sincronizado con openapi.yaml"

# Paso 6: (opcional) Reiniciar backend local si usas uvicorn
Start-Process powershell -ArgumentList "uvicorn main:app --reload" -NoNewWindow
Write-Host "🚀 Uvicorn relanzado con --reload (si usas backend local)"

# Paso 7: (opcional) Lanzar Streamlit para frontend visual
Start-Process powershell -ArgumentList "streamlit run app_streamlit_tabs.py" -NoNewWindow
Write-Host "🚀 Streamlit lanzado"
