[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$baseUrl = "http://localhost:8000"
$outputDir = ".\resultados_api"
if (!(Test-Path $outputDir)) { New-Item -ItemType Directory -Path $outputDir | Out-Null }

# 1. /status/json (GET)
Invoke-RestMethod -Uri "$baseUrl/status/json" | ConvertTo-Json -Depth 10 | Out-File -Encoding UTF8 "$outputDir/status_json.json"

# 2. / (GET)
Invoke-RestMethod -Uri "$baseUrl/" | ConvertTo-Json -Depth 10 | Out-File -Encoding UTF8 "$outputDir/root.json"

# 3. /predict (POST)
$json = @{ texto = "Prueba predictiva legal sobre despido injustificado y fraude laboral" } | ConvertTo-Json
Invoke-RestMethod -Uri "$baseUrl/predict" -Method POST -Body $json -ContentType "application/json" | ConvertTo-Json -Depth 10 | Out-File -Encoding UTF8 "$outputDir/predict.json"

# 4. /api/prediccion/ (POST)
$json = @{ contexto = "El empleador terminó el contrato sin causa, posible fraude y acoso sexual laboral" } | ConvertTo-Json
Invoke-RestMethod -Uri "$baseUrl/api/prediccion/" -Method POST -Body $json -ContentType "application/json" | ConvertTo-Json -Depth 10 | Out-File -Encoding UTF8 "$outputDir/api_prediccion.json"

# 5. /vision/ (POST)
$json = @{ image_id = "IMG_20240526_test" } | ConvertTo-Json
Invoke-RestMethod -Uri "$baseUrl/vision/" -Method POST -Body $json -ContentType "application/json" | ConvertTo-Json -Depth 10 | Out-File -Encoding UTF8 "$outputDir/vision.json"

# 6. /reflexion/ (POST)
$json = @{ documento_analizado = "Ley de Contratos y el Decreto N° 3 sobre procedimientos"; criterios = @("constitucionalidad", "contradicción normativa", "comparado") } | ConvertTo-Json
Invoke-RestMethod -Uri "$baseUrl/reflexion/" -Method POST -Body $json -ContentType "application/json" | ConvertTo-Json -Depth 10 | Out-File -Encoding UTF8 "$outputDir/reflexion.json"

# 7. /forensics/search (GET)
Invoke-RestMethod -Uri "$baseUrl/forensics/search?pregunta=peritaje digital forense" | ConvertTo-Json -Depth 10 | Out-File -Encoding UTF8 "$outputDir/forensics_search.json"

# 8. /text-search (GET)
Invoke-RestMethod -Uri "$baseUrl/text-search?palabra=constitución" | ConvertTo-Json -Depth 10 | Out-File -Encoding UTF8 "$outputDir/text_search.json"

# 9. /legislacion/buscar (GET)
Invoke-RestMethod -Uri "$baseUrl/legislacion/buscar?palabra=trabajo" | ConvertTo-Json -Depth 10 | Out-File -Encoding UTF8 "$outputDir/legislacion_buscar.json"

# 10. /legislacion/norma/{id} (GET)
Invoke-RestMethod -Uri "$baseUrl/legislacion/norma/123" | ConvertTo-Json -Depth 10 | Out-File -Encoding UTF8 "$outputDir/legislacion_norma_123.json"

# 11. /api/bcn/norma/{id} (GET)
Invoke-RestMethod -Uri "$baseUrl/api/bcn/norma/123" | ConvertTo-Json -Depth 10 | Out-File -Encoding UTF8 "$outputDir/api_bcn_norma_123.json"

Write-Output "Todos los endpoints fueron probados y los resultados están en la carpeta $outputDir"
