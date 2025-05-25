# ===============================================
# 🔧 Script de Instalación de Dependencias
# Forensic Legal Cognition 4.1
# ===============================================

param(
    [switch]$Force,
    [switch]$Upgrade
)

$ErrorActionPreference = "Stop"

Write-Host "🔧 Instalando dependencias para Forensic Legal Cognition 4.1" -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan

# Verificar Python
function Test-Python {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "❌ Python no encontrado" -ForegroundColor Red
        Write-Host "   Instala Python 3.11+ desde https://python.org" -ForegroundColor Yellow
        return $false
    }
}

# Verificar/crear entorno virtual
function Initialize-VirtualEnvironment {
    Write-Host "🐍 Configurando entorno virtual..." -ForegroundColor Yellow
    
    if (Test-Path ".venv") {
        if ($Force) {
            Write-Host "🗑️  Eliminando entorno virtual existente..." -ForegroundColor Yellow
            Remove-Item -Recurse -Force ".venv"
        } else {
            Write-Host "📁 Entorno virtual existente encontrado" -ForegroundColor Green
            return $true
        }
    }
    
    Write-Host "📦 Creando nuevo entorno virtual..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error creando entorno virtual" -ForegroundColor Red
        return $false
    }
    
    Write-Host "✅ Entorno virtual creado" -ForegroundColor Green
    return $true
}

# Activar entorno virtual
function Enable-VirtualEnvironment {
    Write-Host "⚡ Activando entorno virtual..." -ForegroundColor Yellow
    
    $activateScript = ".venv\Scripts\Activate.ps1"
    if (-not (Test-Path $activateScript)) {
        Write-Host "❌ Script de activación no encontrado" -ForegroundColor Red
        return $false
    }
    
    try {
        & $activateScript
        Write-Host "✅ Entorno virtual activado" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Error activando entorno virtual: $_" -ForegroundColor Red
        return $false
    }
}

# Instalar dependencias
function Install-Dependencies {
    Write-Host "📦 Instalando dependencias..." -ForegroundColor Yellow
    
    # Actualizar pip
    Write-Host "   Actualizando pip..." -ForegroundColor Gray
    python -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Advertencia: No se pudo actualizar pip" -ForegroundColor Yellow
    }
    
    # Instalar requirements
    if (-not (Test-Path "requirements.txt")) {
        Write-Host "❌ requirements.txt no encontrado" -ForegroundColor Red
        return $false
    }
    
    Write-Host "   Instalando desde requirements.txt..." -ForegroundColor Gray
    if ($Upgrade) {
        python -m pip install --upgrade -r requirements.txt
    } else {
        python -m pip install -r requirements.txt
    }
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error instalando dependencias" -ForegroundColor Red
        return $false
    }
    
    Write-Host "✅ Dependencias instaladas correctamente" -ForegroundColor Green
    return $true
}

# Verificar instalación
function Test-Installation {
    Write-Host "🧪 Verificando instalación..." -ForegroundColor Yellow
    
    # Verificar FastAPI
    try {
        python -c "import fastapi; print(f'FastAPI {fastapi.__version__}')"
        Write-Host "✅ FastAPI instalado correctamente" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Error con FastAPI" -ForegroundColor Red
        return $false
    }
    
    # Verificar otras dependencias críticas
    $criticalPackages = @("uvicorn", "httpx", "beautifulsoup4", "pydantic")
    
    foreach ($package in $criticalPackages) {
        try {
            python -c "import $package"
            Write-Host "✅ $package OK" -ForegroundColor Green
        }
        catch {
            Write-Host "❌ Error con $package" -ForegroundColor Red
            return $false
        }
    }
    
    Write-Host "✅ Instalación verificada correctamente" -ForegroundColor Green
    return $true
}

# Test rápido del servidor
function Test-ServerStart {
    Write-Host "🚀 Probando inicio del servidor..." -ForegroundColor Yellow
    
    try {
        # Importar main para verificar sintaxis
        python -c "from main import app; print('✅ main.py importado correctamente')"
        
        Write-Host "✅ Servidor puede iniciarse correctamente" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Error al importar main.py" -ForegroundColor Red
        Write-Host "   Verifica que todos los módulos estén presentes" -ForegroundColor Yellow
        return $false
    }
}

# Script principal
function Main {
    try {
        # Verificar Python
        if (-not (Test-Python)) {
            exit 1
        }
        
        # Configurar entorno virtual
        if (-not (Initialize-VirtualEnvironment)) {
            exit 1
        }
        
        # Activar entorno virtual
        if (-not (Enable-VirtualEnvironment)) {
            exit 1
        }
        
        # Instalar dependencias
        if (-not (Install-Dependencies)) {
            exit 1
        }
        
        # Verificar instalación
        if (-not (Test-Installation)) {
            exit 1
        }
        
        # Test servidor
        if (-not (Test-ServerStart)) {
            Write-Host "⚠️  Advertencia: Hay problemas con el código, revisa los módulos" -ForegroundColor Yellow
        }
        
        # Resumen final
        Write-Host ""
        Write-Host "🎉 INSTALACIÓN COMPLETADA" -ForegroundColor Green
        Write-Host "=========================" -ForegroundColor Green
        Write-Host "✅ Entorno virtual configurado en .venv" -ForegroundColor Green
        Write-Host "✅ Dependencias instaladas" -ForegroundColor Green
        Write-Host "✅ Instalación verificada" -ForegroundColor Green
        Write-Host ""
        Write-Host "📋 Próximos pasos:" -ForegroundColor Cyan
        Write-Host "   1. Activar entorno: .venv\Scripts\Activate.ps1" -ForegroundColor White
        Write-Host "   2. Iniciar servidor: python launch_backend_render.py" -ForegroundColor White
        Write-Host "   3. Ejecutar tests: python test_api.py --quick" -ForegroundColor White
        Write-Host "   4. Deploy a Render: .\deploy_to_render.ps1" -ForegroundColor White
        Write-Host ""
        Write-Host "🌐 URLs una vez iniciado:" -ForegroundColor Cyan
        Write-Host "   - API: http://localhost:8000" -ForegroundColor White
        Write-Host "   - Docs: http://localhost:8000/docs" -ForegroundColor White
        
    }
    catch {
        Write-Host "❌ Error crítico durante instalación: $_" -ForegroundColor Red
        exit 1
    }
}

# Ejecutar script principal
Main