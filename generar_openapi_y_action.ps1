# ===============================================
# 🔄 Script: Generar openapi.yaml + action.json
# ===============================================

# ⚙️ Variables base
$backendPath = "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend"
$staticPath = Join-Path $backendPath "static"
$yamlPath = Join-Path $staticPath "openapi.yaml"
$actionPath = Join-Path $backendPath "action.json"

# 1️⃣ Contenido mínimo y válido del openapi.yaml
$yaml = @"
openapi: 3.1.0
info:
  title: Forensic Legal Cognition 4.1
  description: API chilena de análisis jurídico automatizado.
  version: "1.0"
servers:
  - url: https://gpt-legal-backend.onrender.com
    description: Render

paths:
  /:
    get:
      operationId: healthCheck
      summary: Check de salud
      responses:
        '200':
          description: OK
components:
  schemas: {}
"@

# 2️⃣ Crear carpeta static si no existe
if (-Not (Test-Path $staticPath)) {
    New-Item -ItemType Directory -Path $staticPath | Out-Null
}

# 3️⃣ Guardar el archivo openapi.yaml
$yaml | Out-File $yamlPath -Encoding utf8
Write-Host "`n✅ openapi.yaml creado correctamente en:"
Write-Host "   $yamlPath"

# 4️⃣ Contenido completo de action.json
$action = @"
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
"@

# 5️⃣ Guardar el archivo action.json
$action | Out-File $actionPath -Encoding utf8
Write-Host "`n✅ action.json creado correctamente en:"
Write-Host "   $actionPath"

# 6️⃣ Verificación online
$onlineUrl = "https://gpt-legal-backend.onrender.com/static/openapi.yaml"
Write-Host "`n🌐 Verificando acceso público a $onlineUrl ..."
try {
    $resp = Invoke-WebRequest -Uri $onlineUrl -UseBasicParsing -TimeoutSec 10
    if ($resp.StatusCode -eq 200) {
        Write-Host "`n🟢 openapi.yaml está accesible en línea y listo para importar en ChatGPT."
    } else {
        Write-Host "`n⚠️ Código HTTP $($resp.StatusCode). Verifica que Render esté online."
    }
} catch {
    Write-Host "`n❌ ERROR: No se pudo acceder a $onlineUrl. ¿Está el backend corriendo en Render?"
}

Read-Host "`nPresiona Enter para cerrar"
