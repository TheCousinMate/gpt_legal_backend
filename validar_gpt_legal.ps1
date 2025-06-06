# =============================
# VALIDACIÓN COMPLETA BACKEND 4.1
# Autor: GPT para Kabir (v4.1)
# Uso: Ejecutar en PowerShell con el backend activo en localhost:8000
# =============================

# 1. Establecer API Key si no está seteada
if (-not $env:OPENAI_API_KEY) {
    $env:OPENAI_API_KEY = Read-Host "Ingresa tu OPENAI_API_KEY (comienza con sk-)"
}

# 2. Endpoint base
$baseUrl = "http://127.0.0.1:8000"

# 3. Función para mostrar respuestas
function Mostrar-Respuesta($titulo, $json) {
    Write-Host "`n🟢 [$titulo] Respuesta:" -ForegroundColor Green
    $json | ConvertTo-Json -Depth 5
}

# 4. Probar estado general
Write-Host "`n✅ Verificando /status/json..."
Invoke-RestMethod -Uri "$baseUrl/status/json" -Method GET | Mostrar-Respuesta "STATUS"

# 5. Pruebas POST corregidas (con estructuras válidas)
$tests = @(
    @{ endpoint = "/predict"; body = '{"prompt": "¿Cuál es la capital de Chile?"}' },
    @{ endpoint = "/reflexion"; body = '{"texto": "Necesito saber si un contrato sin firma tiene validez"}' },
    @{ endpoint = "/interpretar"; body = '{"pregunta": "¿Qué dice el artículo 1545 del Código Civil chileno?"}' },
    @{ endpoint = "/vision"; body = '{"image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Ministerio_Publico_de_Chile.svg/1200px-Ministerio_Publico_de_Chile.svg.png"}' }
)

# 6. Ejecutar pruebas reales
foreach ($test in $tests) {
    $url = "$baseUrl$($test.endpoint)"
    Write-Host "`n🚀 Probando $($test.endpoint)..."
    try {
        $resp = Invoke-RestMethod -Uri $url `
            -Method POST `
            -ContentType "application/json; charset=utf-8" `
            -Body $test.body
        Mostrar-Respuesta $test.endpoint $resp
    } catch {
        Write-Host "❌ Error en $($test.endpoint): $($_.Exception.Message)" -ForegroundColor Red
    }
}
