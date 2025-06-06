
$files = @(
"bcn_parser.py",
"bcn_text_search_parser.py",
"config_map.py",
"forensics_proxy.py",
"interprete.py",
"legislacion_bcn.py",
"motor_predictivo.py",
"prediccion_bayesiana.py",
"predict.py",
"reflexion.py",
"root.py",
"vision_forense.py"
)

$folder = "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules"

foreach ($file in $files) {
    $path = Join-Path $folder $file
    if (Test-Path $path) {
        $content = Get-Content $path -Raw
        if ($content -notmatch "from fastapi import APIRouter") {
            Add-Content -Path $path -Value "`nfrom fastapi import APIRouter`n"
        }
        if ($content -notmatch "router = APIRouter") {
            Add-Content -Path $path -Value "`nrouter = APIRouter()`n"
        }
    }
}
Write-Output "Revisión completada. Se agregaron importaciones si no existían."
