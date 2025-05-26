# Crear el JSON legal
$json = '{ "texto": "existe ambigüedad en la norma aplicable al procedimiento" }'

# Hacer el POST al endpoint predict
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/predict" -Method POST -Body $json -ContentType "application/json"

# Guardar el contenido como JSON limpio
$response.Content | Out-File -Encoding utf8 resultado.json

# Abrir el archivo para inspección
notepad resultado.json
