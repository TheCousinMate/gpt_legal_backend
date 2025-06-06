$reglaForense = @"
# Reglas de aislamiento forense - no usar contexto previo
if 'aislar_contexto' not in locals():
    aislar_contexto = True
"@

$archivos = @{}
$archivos += @{"C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\__init__.py" = Get-Content "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\__init__.py" -Raw }
$archivos += @{"C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\bcn_parser.py" = Get-Content "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\bcn_parser.py" -Raw }
$archivos += @{"C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\bcn_text_search_parser.py" = Get-Content "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\bcn_text_search_parser.py" -Raw }
$archivos += @{"C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\config_map.py" = Get-Content "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\config_map.py" -Raw }
$archivos += @{"C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\forensics_proxy.py" = Get-Content "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\forensics_proxy.py" -Raw }
$archivos += @{"C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\interprete.py" = Get-Content "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\interprete.py" -Raw }
$archivos += @{"C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\legislacion_bcn.py" = Get-Content "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\legislacion_bcn.py" -Raw }
$archivos += @{"C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\motor_predictivo.py" = Get-Content "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\motor_predictivo.py" -Raw }
$archivos += @{"C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\prediccion_bayesiana.py" = Get-Content "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\prediccion_bayesiana.py" -Raw }
$archivos += @{"C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\predict.py" = Get-Content "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\predict.py" -Raw }
$archivos += @{"C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\reflexion.py" = Get-Content "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\reflexion.py" -Raw }
$archivos += @{"C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\root.py" = Get-Content "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\root.py" -Raw }
$archivos += @{"C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\vision_forense.py" = Get-Content "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend\gpt_legal_backend\modules\vision_forense.py" -Raw }

foreach ($archivo in $archivos.Keys) {
    $contenido = $archivos[$archivo]
    if ($contenido -notmatch "aislar_contexto") {
        Add-Content -Path $archivo -Value "`n$reglaForense"
        Write-Output "Regla agregada a: $archivo"
    } else {
        Write-Output "Regla ya presente en: $archivo"
    }
}
