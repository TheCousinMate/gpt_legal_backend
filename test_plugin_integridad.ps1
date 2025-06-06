
Write-Host "🔎 Verificando plugin Forensic Legal Cognition 4.1..." -ForegroundColor Cyan

# 1. Verificar ai-plugin.json
$pluginUrl = "https://gpt-legal-backend.onrender.com/.well-known/ai-plugin.json"
$plugin = Invoke-RestMethod -Uri $pluginUrl -Method Get -ErrorAction Stop

if ($plugin.api.url -eq "https://gpt-legal-backend.onrender.com/static/openapi.yaml") {
    Write-Host "✅ ai-plugin.json OK: apunta al openapi.yaml correcto" -ForegroundColor Green
} else {
    Write-Host "❌ ERROR: ai-plugin.json no apunta al openapi.yaml esperado" -ForegroundColor Red
}

# 2. Verificar openapi.yaml
try {
    $openapi = Invoke-WebRequest -Uri "https://gpt-legal-backend.onrender.com/static/openapi.yaml" -Method Get -ErrorAction Stop
    if ($openapi.StatusCode -eq 200) {
        Write-Host "✅ openapi.yaml accesible correctamente" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ ERROR: openapi.yaml no está accesible" -ForegroundColor Red
}

# 3. Verificar /status/json
try {
    $status = Invoke-RestMethod -Uri "https://gpt-legal-backend.onrender.com/status/json" -Method Get -ErrorAction Stop
    if ($status.status -eq "activo") {
        Write-Host "✅ /status/json responde correctamente (activo)" -ForegroundColor Green
    } else {
        Write-Host "❌ /status/json no responde con estado esperado" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ ERROR: /status/json no respondió" -ForegroundColor Red
}

# 4. Verificar logo.png (opcional)
try {
    $logo = Invoke-WebRequest -Uri "https://gpt-legal-backend.onrender.com/logo.png" -Method Head -ErrorAction Stop
    if ($logo.StatusCode -eq 200) {
        Write-Host "✅ logo.png accesible (opcional)" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ logo.png no encontrado (opcional)" -ForegroundColor Yellow
}

Write-Host "🧩 Verificación terminada." -ForegroundColor Cyan
Pause
