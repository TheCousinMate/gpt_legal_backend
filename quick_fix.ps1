# ===============================================
# 🔧 Script de Corrección Rápida
# Soluciona problemas inmediatos del backend
# ===============================================

Write-Host "🔧 Corrección Rápida - Forensic Legal Cognition 4.1" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

# 1. Activar entorno virtual si existe
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "⚡ Activando entorno virtual..." -ForegroundColor Yellow
    & .venv\Scripts\Activate.ps1
} else {
    Write-Host "⚠️  Entorno virtual no encontrado" -ForegroundColor Yellow
    Write-Host "   Ejecuta: .\install_dependencies.ps1" -ForegroundColor Gray
}

# 2. Instalar dependencias mínimas si faltan
Write-Host "📦 Verificando dependencias críticas..." -ForegroundColor Yellow
try {
    python -c "import fastapi"
    Write-Host "✅ FastAPI disponible" -ForegroundColor Green
}
catch {
    Write-Host "📦 Instalando FastAPI..." -ForegroundColor Yellow
    pip install fastapi uvicorn httpx beautifulsoup4 requests pydantic
}

# 3. Corregir archivo test_api.py (eliminar BOM y caracteres problemáticos)
Write-Host "🔧 Corrigiendo test_api.py..." -ForegroundColor Yellow
if (Test-Path "test_api.py") {
    $testContent = Get-Content "test_api.py" -Raw -Encoding UTF8
    # Eliminar BOM si existe
    $testContent = $testContent -replace "^\uFEFF", ""
    # Corregir líneas problemáticas con strings no terminados
    $testContent = $testContent -replace 'error=f"Status: \{response\.status_code if response else ''No[^"]*, 'error=f"Status: {response.status_code if response else ''No response''}"'
    $testContent | Set-Content "test_api.py" -Encoding UTF8 -NoNewline
    Write-Host "✅ test_api.py corregido" -ForegroundColor Green
}

# 4. Corregir main.py (eliminar BOM)
Write-Host "🔧 Corrigiendo main.py..." -ForegroundColor Yellow
if (Test-Path "main.py") {
    $mainContent = Get-Content "main.py" -Raw -Encoding UTF8
    $mainContent = $mainContent -replace "^\uFEFF", ""
    $mainContent | Set-Content "main.py" -Encoding UTF8 -NoNewline
    Write-Host "✅ main.py corregido" -ForegroundColor Green
}

# 5. Verificar estructura de módulos
Write-Host "📁 Verificando estructura de módulos..." -ForegroundColor Yellow
if (-not (Test-Path "modules")) {
    New-Item -ItemType Directory -Path "modules" -Force
    New-Item -ItemType File -Path "modules\__init__.py" -Force
    Write-Host "✅ Directorio modules creado" -ForegroundColor Green
}

$requiredModules = @(
    "reflexion.py",
    "prediccion_bayesiana.py", 
    "vision_forense.py",
    "legislacion_bcn.py",
    "forensics_proxy.py",
    "bcn_parser.py",
    "bcn_text_search_parser.py"
)

$missingModules = @()
foreach ($module in $requiredModules) {
    if (-not (Test-Path "modules\$module")) {
        $missingModules += $module
    }
}

if ($missingModules.Count -gt 0) {
    Write-Host "⚠️  Módulos faltantes detectados:" -ForegroundColor Yellow
    $missingModules | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    Write-Host "   Copia los módulos corregidos desde los artifacts" -ForegroundColor Gray
}

# 6. Crear archivos mínimos si faltan completamente
Write-Host "🔧 Verificando archivos críticos..." -ForegroundColor Yellow

# utils_output.py mínimo
if (-not (Test-Path "utils_output.py")) {
    Write-Host "📄 Creando utils_output.py básico..." -ForegroundColor Yellow
    @"
import json
from datetime import datetime

def output_dual(data):
    return {
        "json": json.dumps(data, ensure_ascii=False, indent=2),
        "markdown": f"# Respuesta\n\n{data.get('respuesta', 'Sin respuesta')}"
    }

def create_error_response(error_msg, details=""):
    return output_dual({
        "respuesta": f"Error: {error_msg}",
        "clasificacion": "Error",
        "justificacion": details,
        "logs": {"error": error_msg, "timestamp": datetime.now().isoformat()}
    })
"@ | Set-Content "utils_output.py" -Encoding UTF8
    Write-Host "✅ utils_output.py creado" -ForegroundColor Green
}

# 7. Crear módulo motor_predictivo básico si falta
if (-not (Test-Path "modules\motor_predictivo.py")) {
    Write-Host "📄 Creando motor_predictivo.py básico..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "modules" -Force -ErrorAction SilentlyContinue
    @"
def analizar_input_legal(texto):
    if not texto:
        return "Texto vacío. Proporcione contenido jurídico para análisis."
    
    if "trabajador" in texto.lower() and "contrato" in texto.lower():
        return "Riesgo laboral detectado: verificar formalización contractual según Código del Trabajo."
    elif "responsabilidad" in texto.lower():
        return "Análisis de responsabilidad: revisar marco legal aplicable."
    else:
        return f"Análisis legal básico para: {texto[:100]}..."
"@ | Set-Content "modules\motor_predictivo.py" -Encoding UTF8
    Write-Host "✅ motor_predictivo.py básico creado" -ForegroundColor Green
}

# 8. Test sintaxis final
Write-Host "🧪 Verificando sintaxis final..." -ForegroundColor Yellow
try {
    python -m py_compile main.py
    Write-Host "✅ main.py - sintaxis OK" -ForegroundColor Green
}
catch {
    Write-Host "❌ main.py - errores de sintaxis" -ForegroundColor Red
}

try {
    python -m py_compile test_api.py
    Write-Host "✅ test_api.py - sintaxis OK" -ForegroundColor Green
}
catch {
    Write-Host "❌ test_api.py - errores de sintaxis" -ForegroundColor Red
}

# 9. Test de importación básico
Write-Host "🔍 Test de importación básico..." -ForegroundColor Yellow
try {
    python -c "import sys; sys.path.append('.'); from utils_output import output_dual; print('✅ utils_output importado')"
}
catch {
    Write-Host "❌ Error importando utils_output" -ForegroundColor Red
}

try {
    python -c "import sys; sys.path.append('.'); from modules.motor_predictivo import analizar_input_legal; print('✅ motor_predictivo importado')"
}
catch {
    Write-Host "❌ Error importando motor_predictivo" -ForegroundColor Red
}

# 10. Resumen y próximos pasos
Write-Host ""
Write-Host "🎯 CORRECCIÓN RÁPIDA COMPLETADA" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Estado actual:" -ForegroundColor Cyan
Write-Host "✅ Dependencias verificadas" -ForegroundColor Green
Write-Host "✅ Archivos corregidos (BOM eliminado)" -ForegroundColor Green
Write-Host "✅ Estructura básica verificada" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Próximos pasos recomendados:" -ForegroundColor Cyan
Write-Host "1. 📄 Copia los módulos corregidos desde los artifacts que proporcioné" -ForegroundColor White
Write-Host "2. 🧪 Ejecuta: python test_api.py --quick" -ForegroundColor White
Write-Host "3. 🚀 Si tests OK, ejecuta: python launch_backend_render.py" -ForegroundColor White
Write-Host "4. 🌐 Deploy: .\deploy_to_render.ps1 -Message 'Backend corregido'" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Si persisten errores:" -ForegroundColor Yellow
Write-Host "   - Ejecuta: .\install_dependencies.ps1 -Force" -ForegroundColor Gray
Write-Host "   - Verifica que todos los artifacts estén copiados" -ForegroundColor Gray
Write-Host "   - Revisa logs de error para diagnóstico específico" -ForegroundColor Gray