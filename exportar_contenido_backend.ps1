# ===============================================
# 📦 Exportador completo de contenido del backend
# ===============================================

$rootPath = "C:\Users\khazb\OneDrive\Escritorio\Documentos\gpt_legal_backend"
$outputFile = Join-Path $rootPath "reporte_backend.txt"
$extensions = @(".py", ".json", ".yaml", ".yml", ".env", ".md", ".txt", ".html", ".js", ".ts", ".bat", ".ps1")

# 🧹 Borra archivo anterior si existe
if (Test-Path $outputFile) {
    Remove-Item $outputFile
}

"🔎 Reporte generado automáticamente - $(Get-Date)" | Out-File $outputFile -Encoding UTF8
"Ruta base: $rootPath`n" | Out-File $outputFile -Append

# 🔁 Recorre todos los archivos con extensiones reconocidas
Get-ChildItem -Path $rootPath -Recurse -File | Where-Object { $extensions -contains $_.Extension.ToLower() } | ForEach-Object {
    $file = $_
    $fullPath = $file.FullName
    $relPath = $fullPath.Substring($rootPath.Length).TrimStart('\')
    $content = Get-Content -Path $fullPath -Raw -ErrorAction SilentlyContinue

    # 📄 Encabezado por archivo
    "====================================================" | Out-File $outputFile -Append
    "📄 Archivo: $($file.Name)" | Out-File $outputFile -Append
    "📂 Ruta: $relPath" | Out-File $outputFile -Append
    "📦 Tamaño: $($file.Length) bytes" | Out-File $outputFile -Append
    "====================================================" | Out-File $outputFile -Append
    "" | Out-File $outputFile -Append

    if (-not $content) {
        "⚠️ Archivo vacío o no legible." | Out-File $outputFile -Append
    } else {
        $content | Out-File $outputFile -Append
    }

    "`n`n" | Out-File $outputFile -Append
}

Write-Host "`n✅ Reporte generado:"
Write-Host "   $outputFile"

Read-Host "`nPresiona Enter para cerrar"
