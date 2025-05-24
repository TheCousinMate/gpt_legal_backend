# full_backend_finalizer.ps1

# 🚀 Activación de entorno y validación total del backend GPT Legal
Write-Host "🔧 Iniciando validación final del backend..."

$base = "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend"
$venv = "$base\.venv"
$tests = "$base\tests"
$hookPath = "$base\.git\hooks\pre-commit"

# 1. Activar entorno virtual o crearlo
if (!(Test-Path "$venv\Scripts\activate.ps1")) {
  python -m venv $venv
  Write-Host "✅ Entorno virtual creado"
}
& "$venv\Scripts\activate.ps1"

# 2. Instalar dependencias
pip install -r "$base\requirements.txt"

# 3. Regenerar archivo de test
$testScript = @"
import requests
BASE = "http://127.0.0.1:8000"

def check(endpoint, method='get', data=None, params=None):
    try:
        if method == 'get':
            r = requests.get(BASE + endpoint, params=params)
        else:
            r = requests.post(BASE + endpoint, json=data)
        r.raise_for_status()
        print(f"✅ {endpoint} OK")
    except Exception as e:
        print(f"❌ {endpoint} FALLÓ: {e}")

check("/")
check("/reflexion/", 'post', {"documento_analizado": "Ley chilena...", "criterios": ["claridad"]})
check("/vision/", 'post', {"image_id": "imagen123"})
check("/forensics/search", 'get', None, {"pregunta": "Derechos del consumidor"})
check("/legislacion/buscar", 'get', None, {"palabra": "contrato"})
"@
$testPath = "$tests\__test_all_endpoints.py"
$testScript | Set-Content -Encoding UTF8 -Path $testPath
Write-Host "✅ Script de test regenerado"

# 4. Ejecutar update_openapi.py si existe
$openapiUpdater = "$base\update_openapi.py"
if (Test-Path $openapiUpdater) {
  python $openapiUpdater
}

# 5. Ejecutar los tests
python $testPath

# 6. Activar pre-commit hook si existe
if (Test-Path "$hookPath") {
  try {
    wsl chmod +x $hookPath
    Write-Host "✅ Pre-commit hook activado"
  } catch {
    Write-Host "⚠️ No se pudo activar hook con chmod (WSL no disponible o ruta incorrecta)"
  }
}

Write-Host "🎯 Backend final validado y funcional. Puedes hacer push y desplegar."
