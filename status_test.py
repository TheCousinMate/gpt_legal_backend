import requests

URL = "http://127.0.0.1:8000/status/json"  # o https://gpt-legal-backend.onrender.com/status/json si ya está online
HEADERS = {
    "x-api-key": "FL4.1-1112919"  # Debe coincidir con tu API_KEY_SECRET en el .env
}

response = requests.get(URL, headers=HEADERS)

print("Código de estado:", response.status_code)
print("Respuesta JSON:", response.json())
