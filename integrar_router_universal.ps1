
$routerPath = "modules/router_universal.py"
$mainPath = "main.py"

# Verificar si la línea ya está importada
$importLine = "from modules.router_universal import router as universal_router"
$includeLine = "app.include_router(universal_router, prefix='/router')"

if (-not (Get-Content $mainPath | Select-String -Pattern $importLine)) {
    Add-Content -Path $mainPath -Value "`n$importLine"
}

if (-not (Get-Content $mainPath | Select-String -Pattern $includeLine)) {
    Add-Content -Path $mainPath -Value "$includeLine"
}

Write-Output "Integración completa del router_universal.py"
