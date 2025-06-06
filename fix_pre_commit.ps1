# fix_pre_commit.ps1

# 1. Crear directorio .githooks si no existe
$hookDir = ".githooks"
if (-not (Test-Path $hookDir)) {
    New-Item -ItemType Directory -Path $hookDir | Out-Null
    Write-Host "✅ Carpeta .githooks creada."
} else {
    Write-Host "🔁 Carpeta .githooks ya existía."
}

# 2. Escribir contenido del hook PowerShell
$psHookPath = "$hookDir/pre-commit.ps1"
$psHookContent = @'
#!/usr/bin/env pwsh

# ✅ Pre-commit hook para proteger secretos y validar backend (versión PowerShell)

# 1. Bloqueo de archivos .txt sensibles en /static/
$archivos = git diff --cached --name-only
foreach ($archivo in $archivos) {
    if ($archivo -match '^static/.*\.txt$') {
        Write-Host "❌ ERROR: No se permite hacer commit de archivos .txt en /static/"
        exit 1
    }
}

# 2. Verifica existencia de .env
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  Advertencia: No se encontró .env en el proyecto."
}

# 3. Validación de sintaxis Python
Write-Host "🔍 Validando sintaxis..."
$valid = python -m compileall .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR: Hay errores de sintaxis Python. Corrige antes de hacer commit."
    exit 1
}

Write-Host "✅ Pre-commit validado. Todo OK."
exit 0
'@

$psHookContent | Set-Content -Encoding UTF8 -Path $psHookPath
Write-Host "✅ Hook PowerShell generado: $psHookPath"

# 3. Crear wrapper Bash en .git/hooks que llama al script de PowerShell
$wrapperPath = ".git/hooks/pre-commit"
$wrapperContent = "#!/bin/sh\npwsh .githooks/pre-commit.ps1"
$wrapperContent | Set-Content -Encoding UTF8 -Path $wrapperPath
Write-Host "✅ Wrapper bash en .git/hooks/pre-commit creado."

# 4. Asignar permisos ejecutables (si WSL está disponible)
try {
    wsl chmod +x .git/hooks/pre-commit
    Write-Host "🔒 Permisos ejecutables asignados vía WSL."
} catch {
    Write-Host "⚠️  No se pudo aplicar chmod. Verifica manualmente si es necesario."
}

# 5. Configurar Git para usar .githooks como ruta oficial
git config core.hooksPath .githooks
Write-Host "🛠️ Git configurado para usar .githooks"

Write-Host "🎯 Hook pre-commit listo y funcional. Testéalo haciendo un commit."
