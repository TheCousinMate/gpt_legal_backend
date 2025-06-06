# Rutas
$backendPath = "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend"
$pluginPath = "$backendPath\forensic_legal_plugin"
$wellKnownPath = "$pluginPath\.well-known"
$mainFile = "$backendPath\main.py"
$aiPluginSource = "$pluginPath\plugin.json"
$aiPluginDest = "$wellKnownPath\ai-plugin.json"

# Crear .well-known si no existe
if (-not (Test-Path $wellKnownPath)) {
    New-Item -ItemType Directory -Path $wellKnownPath | Out-Null
    Write-Output "✔️ Carpeta .well-known creada"
}

# Copiar plugin.json como ai-plugin.json
if (Test-Path $aiPluginSource) {
    Copy-Item -Path $aiPluginSource -Destination $aiPluginDest -Force
    Write-Output "✅ plugin.json copiado como ai-plugin.json"
} else {
    Write-Output "⚠️ No se encontró plugin.json en $pluginPath"
}

# Añadir bloque a main.py si no existe
$mainContent = Get-Content $mainFile -Raw
if ($mainContent -notmatch 'app\.mount\("/\.well-known"') {
    $block = @"
from fastapi.staticfiles import StaticFiles
import os
plugin_dir = os.path.join(os.path.dirname(__file__), "forensic_legal_plugin", ".well-known")
if os.path.exists(plugin_dir):
    app.mount("/.well-known", StaticFiles(directory=plugin_dir), name="static")
"@
    Add-Content -Path $mainFile -Value $block
    Write-Output "🛠️ Bloque para exponer /.well-known agregado a main.py"
} else {
    Write-Output "✅ main.py ya contiene el montaje de /.well-known"
}

# Confirmación
Write-Output "`n🚀 Plugin operativo y vinculado"
Write-Output "🔗 Prueba: http://localhost:8000/.well-known/ai-plugin.json"
