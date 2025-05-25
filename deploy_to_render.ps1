# ===============================================
# 🚀 Script de Deployment para Render
# Forensic Legal Cognition 4.1
# ===============================================

param(
    [switch]$Force,
    [switch]$Test,
    [string]$Message = "Automated deployment $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
)

$ErrorActionPreference = "Stop"

# Configuración
$ProjectPath = $PSScriptRoot
$RequiredFiles = @(
    "main.py",
    "requirements.txt", 
    "Dockerfile",
    "launch_backend_render.py",
    "utils_output.py",
    "openapi.yaml",
    "action.json"
)

Write-Host "🔧 Forensic Legal Cognition 4.1 - Deployment Script" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

# Función para verificar archivos
function Test-RequiredFiles {
    Write-Host "📋 Verificando archivos requeridos..." -ForegroundColor Yellow
    
    $missing = @()
    foreach ($file in $RequiredFiles) {
        $path = Join-Path $ProjectPath $file
        if (-not (Test-Path $path)) {
            $missing += $file
        } else {
            Write-Host "   ✅ $file" -ForegroundColor Green
        }
    }
    
    if ($missing.Count -gt 0) {
        Write-Host "❌ Archivos faltantes:" -ForegroundColor Red
        $missing | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
        return $false
    }
    
    Write-Host "✅ Todos los archivos requeridos están presentes" -ForegroundColor Green
    return $true
}

# Función para validar sintaxis Python
function Test-PythonSyntax {
    Write-Host "🐍 Validando sintaxis Python..." -ForegroundColor Yellow
    
    try {
        $result = python -m py_compile main.py 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Error de sintaxis en main.py:" -ForegroundColor Red
            Write-Host $result -ForegroundColor Red
            return $false
        }
        
        # Verificar módulos
        $moduleFiles = Get-ChildItem -Path "modules" -Filter "*.py" -ErrorAction SilentlyContinue
        foreach ($module in $moduleFiles) {
            $result = python -m py_compile $module.FullName 2>&1
            if ($LASTEXITCODE -ne 0) {
                Write-Host "❌ Error de sintaxis en $($module.Name):" -ForegroundColor Red
                Write-Host $result -ForegroundColor Red
                return $false
            }
        }
        
        Write-Host "✅ Sintaxis Python validada" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Error al validar sintaxis: $_" -ForegroundColor Red
        return $false
    }
}

# Función para generar OpenAPI
function Update-OpenAPISpec {
    Write-Host "📄 Actualizando especificación OpenAPI..." -ForegroundColor Yellow
    
    try {
        # Verificar si existe update_openapi.py
        if (Test-Path "update_openapi.py") {
            python update_openapi.py
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ OpenAPI actualizado" -ForegroundColor Green
            } else {
                Write-Host "⚠️  Advertencia: No se pudo actualizar OpenAPI automáticamente" -ForegroundColor Yellow
            }
        } else {
            Write-Host "⚠️  update_openapi.py no encontrado, usando openapi.yaml existente" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "⚠️  Error al actualizar OpenAPI: $_" -ForegroundColor Yellow
    }
}

# Función para ejecutar tests
function Invoke-Tests {
    if (-not $Test) {
        return $true
    }
    
    Write-Host "🧪 Ejecutando tests..." -ForegroundColor Yellow
    
    try {
        if (Test-Path "test_api.py") {
            python test_api.py --quick
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Tests pasaron correctamente" -ForegroundColor Green
                return $true
            } else {
                Write-Host "❌ Tests fallaron" -ForegroundColor Red
                return $false
            }
        } else {
            Write-Host "⚠️  test_api.py no encontrado, saltando tests" -ForegroundColor Yellow
            return $true
        }
    }
    catch {
        Write-Host "❌ Error ejecutando tests: $_" -ForegroundColor Red
        return $false
    }
}

# Función para commit y push
function Invoke-GitDeployment {
    Write-Host "📦 Preparando deployment Git..." -ForegroundColor Yellow
    
    try {
        # Verificar estado Git
        $status = git status --porcelain 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Error al verificar estado Git: $status" -ForegroundColor Red
            return $false
        }
        
        if (-not $status -and -not $Force) {
            Write-Host "ℹ️  No hay cambios para hacer commit" -ForegroundColor Blue
            return $true
        }
        
        # Añadir archivos
        git add .
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Error al añadir archivos a Git" -ForegroundColor Red
            return $false
        }
        
        # Commit
        git commit -m $Message
        if ($LASTEXITCODE -ne 0 -and -not $Force) {
            Write-Host "❌ Error al hacer commit" -ForegroundColor Red
            return $false
        }
        
        # Push
        Write-Host "🚀 Pushing to repository..." -ForegroundColor Yellow
        git push origin main
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Error al hacer push" -ForegroundColor Red
            return $false
        }
        
        Write-Host "✅ Deployment Git completado" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Error en deployment Git: $_" -ForegroundColor Red
        return $false
    }
}

# Función para verificar deployment en Render
function Test-RenderDeployment {
    Write-Host "🌐 Verificando deployment en Render..." -ForegroundColor Yellow
    
    $renderUrl = "https://gpt-legal-backend.onrender.com"
    $maxAttempts = 10
    $delay = 30
    
    for ($i = 1; $i -le $maxAttempts; $i++) {
        try {
            Write-Host "   Intento $i/$maxAttempts..." -ForegroundColor Gray
            
            $response = Invoke-WebRequest -Uri "$renderUrl/" -TimeoutSec 30 -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ Deployment en Render verificado exitosamente" -ForegroundColor Green
                
                # Verificar contenido de respuesta
                $content = $response.Content | ConvertFrom-Json
                if ($content.status -eq "alive") {
                    Write-Host "✅ API respondiendo correctamente" -ForegroundColor Green
                    Write-Host "   Versión: $($content.version)" -ForegroundColor Gray
                    return $true
                }
            }
        }
        catch {
            Write-Host "   ⏳ Esperando deployment... ($delay segundos)" -ForegroundColor Yellow
            Start-Sleep $delay
        }
    }
    
    Write-Host "⚠️  No se pudo verificar el deployment automáticamente" -ForegroundColor Yellow
    Write-Host "   Revisa manualmente: $renderUrl" -ForegroundColor Yellow
    return $false
}

# Script principal
function Main {
    try {
        Set-Location $ProjectPath
        
        # Verificaciones pre-deployment
        if (-not (Test-RequiredFiles)) {
            Write-Host "❌ Deployment cancelado: archivos faltantes" -ForegroundColor Red
            exit 1
        }
        
        if (-not (Test-PythonSyntax)) {
            Write-Host "❌ Deployment cancelado: errores de sintaxis" -ForegroundColor Red
            exit 1
        }
        
        # Actualizaciones
        Update-OpenAPISpec
        
        # Tests opcionales
        if (-not (Invoke-Tests)) {
            Write-Host "❌ Deployment cancelado: tests fallaron" -ForegroundColor Red
            exit 1
        }
        
        # Git deployment
        if (-not (Invoke-GitDeployment)) {
            Write-Host "❌ Deployment fallido en Git" -ForegroundColor Red
            exit 1
        }
        
        # Verificar deployment en Render
        Write-Host "⏳ Esperando que Render procese el deployment..." -ForegroundColor Yellow
        Start-Sleep 60  # Dar tiempo a Render para iniciar
        
        Test-RenderDeployment
        
        # Resumen final
        Write-Host ""
        Write-Host "🎉 DEPLOYMENT COMPLETADO" -ForegroundColor Green
        Write-Host "========================" -ForegroundColor Green
        Write-Host "✅ API URL: https://gpt-legal-backend.onrender.com" -ForegroundColor Green
        Write-Host "✅ OpenAPI: https://gpt-legal-backend.onrender.com/static/openapi.yaml" -ForegroundColor Green
        Write-Host "✅ Docs: https://gpt-legal-backend.onrender.com/docs" -ForegroundColor Green
        Write-Host ""
        Write-Host "📋 Próximos pasos:" -ForegroundColor Cyan
        Write-Host "   1. Verificar API en el navegador" -ForegroundColor White
        Write-Host "   2. Ejecutar tests completos: python test_api.py" -ForegroundColor White
        Write-Host "   3. Actualizar Custom GPT con nueva URL si es necesario" -ForegroundColor White
        
    }
    catch {
        Write-Host "❌ Error crítico durante deployment: $_" -ForegroundColor Red
        exit 1
    }
}

# Ejecutar script principal
Main