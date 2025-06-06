#!/usr/bin/env pwsh
# 📜 Script: deploy_backend.ps1
# Autor: GPT para Kabir (Forensic Legal Cognition 4.1)
# Descripción: Automatiza limpieza, instalación y despliegue completo del backend

# 🔧 Parámetros
$BackendRoot = "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend"
$StaticDir = Join-Path $BackendRoot "static"
$ModulesDir = Join-Path $BackendRoot "modules"
$VenvDirs = @(".venv", "__pycache__", "site-packages")
$TempLog = Join-Path $BackendRoot "deploy_log.txt"

Write-Host "🔁 Iniciando limpieza de entorno..."
foreach ($dir in $VenvDirs) {
    $full = Join-Path $BackendRoot $dir
    if (Test-Path $full) {
        Remove-Item -Path $full -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "🧹 Eliminado: $dir"
    }
}

Write-Host "📦 Verificando módulos esenciales..."
$ExpectedModules = @(
    "reflexion.py", "vision_forense.py", "predict.py", "forensics_proxy.py",
    "legislacion_bcn.py", "bcn_parser.py", "bcn_text_search_parser.py", "prediccion_bayesiana.py",
    "root.py", "router_universal.py", "interprete.py", "corpus_legal.py", "motor_predictivo.py", "status.py"
)

foreach ($mod in $ExpectedModules) {
    $path = Join-Path $ModulesDir $mod
    if (-not (Test-Path $path)) {
        Write-Host "⚠️ FALTA MÓDULO: $mod" -ForegroundColor Red
    }
}

Write-Host "📚 Instalando dependencias..."
pip install -r (Join-Path $BackendRoot "requirements.txt") | Out-File -FilePath $TempLog -Append

Write-Host "🚀 Ejecutando backend (modo desarrollo)..."
cd $BackendRoot
Start-Process "uvicorn" -ArgumentList "main:app --reload" -NoNewWindow

Write-Host "✅ Backend desplegado en modo live. Verifica logs y funcionamiento."
Write-Host "📄 openapi.yaml y ai-plugin.json deben estar en: $StaticDir"

# FIN
