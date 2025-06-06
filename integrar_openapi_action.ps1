# 📁 Variables
$BackendPath = "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend"
$StaticPath = Join-Path $BackendPath "static"
$OpenAPIFile = Join-Path $StaticPath "openapi.yaml"
$ActionFile = Join-Path $BackendPath "action.json"

# 🧪 Verificar existencia del schema
if (-Not (Test-Path $OpenAPIFile)) {
    Write-Host "❌ ERROR: No se encontró el archivo 'openapi.yaml' en $StaticPath"
    exit 1
}

# 📄 Generar archivo action.json con URLs coherentes (Render)
@"
{
  "schema_version": "v1",
  "name_for_human": "Forensic Legal Cognition",
  "name_for_model": "forensicLegalCognition",
  "description_for_human": "Consulta y análisis jurídico automatizado del derecho chileno.",
  "description_for_model": "Utiliza esta API para hacer análisis legales, predictivos y forenses de documentos jurídicos chilenos.",
  "auth": {
    "type": "none"
  },
  "api": {
    "type": "openapi",
    "url": "https://gpt-legal-backend.onrender.com/static/openapi.yaml"
  },
  "logo_url": "https://raw.githubusercontent.com/TheCousinMate/gpt_legal_backend/main/static/logo.png",
  "contact_email": "kharzun@gmail.com",
  "legal_info_url": "https://github.com/TheCousinMate/gpt_legal_backend#terms"
}
"@ | Out-File $ActionFile -Encoding utf8

# ✅ Confirmación
Write-Host "`n🎉 Archivo 'action.json' creado exitosamente en:`n$ActionFile"
Write-Host "`n📎 Enlace OpenAPI que se usará en producción:"
Write-Host "   https://gpt-legal-backend.onrender.com/static/openapi.yaml"
