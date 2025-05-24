# ✅ SCRIPT POWERSHELL AUTOMATIZADO: VALIDACIÓN COMPLETA BACKEND GPT LEGAL
# Ejecuta todo el proceso en un solo comando

$base = "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend"
$modules = "$base\modules"
$tests = "$base\tests"

# 1. Corregir prefix en routers
(Get-Content "$modules\forensics_proxy.py") -replace 'APIRouter\(\)', 'APIRouter(prefix="/forensics")' | Set-Content -Encoding UTF8 -Path "$modules\forensics_proxy.py"
(Get-Content "$modules\legislacion_bcn.py") -replace 'APIRouter\(\)', 'APIRouter(prefix="/legislacion")' | Set-Content -Encoding UTF8 -Path "$modules\legislacion_bcn.py"
Write-Host "✅ Prefixes corregidos"

# 2. Verificar e insertar endpoint /search si no existe
$content = Get-Content "$modules\forensics_proxy.py" -Raw
if ($content -notmatch "/search") {
    Add-Content -Encoding UTF8 -Path "$modules\forensics_proxy.py" -Value @'
@router.get("/search")
def buscar_forensics(pregunta: str):
    return {"respuesta": f"Simulación de búsqueda forense para: {pregunta}"}
'@
    Write-Host "✅ Endpoint /search añadido a forensics_proxy.py"
} else {
    Write-Host "🔁 Endpoint /search ya presente en forensics_proxy.py"
}

# 3. Regenerar archivo de test
$test_script = @"
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
$test_path = "$tests\__test_all_endpoints.py"
$test_script | Set-Content -Encoding UTF8 -Path $test_path
Write-Host "✅ Script de test regenerado"

# 4. Ejecutar generación de OpenAPI
python "$base\update_openapi.py"

# 5. Ejecutar test
python $test_path

Write-Host "`n🎯 Validación automatizada completada. Revisa arriba los estados de cada endpoint."
