[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$resultDir = ".\resultados_api"
if (-not (Test-Path $resultDir)) { New-Item -ItemType Directory -Path $resultDir | Out-Null }

function Save-Result($name, $result) {
    $file = Join-Path $resultDir "$name.json"
    $result | ConvertTo-Json -Depth 10 | Out-File -Encoding UTF8 $file
    Write-Output "[$name] => OK, guardado en $file"
}

try { $r = Invoke-RestMethod -Uri "http://localhost:8000/status/json"; Save-Result "status_json" $r } catch { Write-Output "[status_json] ERROR: $_" }
try { $r = Invoke-RestMethod -Uri "http://localhost:8000/"; Save-Result "root" $r } catch { Write-Output "[root] ERROR: $_" }
try { $r = Invoke-RestMethod -Uri "http://localhost:8000/legislacion/buscar?palabra=trabajo"; Save-Result "legislacion_buscar" $r } catch { Write-Output "[legislacion_buscar] ERROR: $_" }
try { $r = Invoke-RestMethod -Uri "http://localhost:8000/forensics/search?pregunta=peritaje"; Save-Result "forensics_search" $r } catch { Write-Output "[forensics_search] ERROR: $_" }
try { $r = Invoke-RestMethod -Uri "http://localhost:8000/text-search?palabra=constitución"; Save-Result "text_search" $r } catch { Write-Output "[text_search] ERROR: $_" }
try { $r = Invoke-RestMethod -Uri "http://localhost:8000/legislacion/norma/123"; Save-Result "legislacion_norma_123" $r } catch { Write-Output "[legislacion_norma_123] ERROR: $_" }
try { $r = Invoke-RestMethod -Uri "http://localhost:8000/api/bcn/norma/123"; Save-Result "api_bcn_norma_123" $r } catch { Write-Output "[api_bcn_norma_123] ERROR: $_" }

$json = @{ contexto = "Existe ambigüedad en la norma aplicable al procedimiento" } | ConvertTo-Json
try { $r = Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method POST -Body $json -ContentType "application/json"; Save-Result "predict" $r } catch { Write-Output "[predict] ERROR: $_" }

$json = @{ contexto = "Predicción sobre resultado de demanda laboral" } | ConvertTo-Json
try { $r = Invoke-RestMethod -Uri "http://localhost:8000/api/prediccion/" -Method POST -Body $json -ContentType "application/json"; Save-Result "api_prediccion" $r } catch { Write-Output "[api_prediccion] ERROR: $_" }

$json = @{
    texto = "Visión general de la evolución normativa en Chile"
    image_id = "img_test"
} | ConvertTo-Json
try { $r = Invoke-RestMethod -Uri "http://localhost:8000/vision/" -Method POST -Body $json -ContentType "application/json"; Save-Result "vision" $r } catch { Write-Output "[vision] ERROR: $_" }

$json = @{
    texto = "Reflexión jurídica sobre la prescripción en derecho civil chileno"
    documento_analizado = "Ley 123 sobre prescripción"
    criterios = "jurídicos"
} | ConvertTo-Json
try { $r = Invoke-RestMethod -Uri "http://localhost:8000/reflexion/" -Method POST -Body $json -ContentType "application/json"; Save-Result "reflexion" $r } catch { Write-Output "[reflexion] ERROR: $_" }

Write-Output "Pruebas completas. Revisa carpeta $resultDir para los resultados."
