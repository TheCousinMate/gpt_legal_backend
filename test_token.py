import requests

url = "http://127.0.0.1:8000/status/json"
headers = {
    "x-api-key": "FL4.1-1112919"  # debe coincidir con tu .env
}

r = requests.get(url, headers=headers)
print("Código de estado:", r.status_code)
print("Respuesta:", r.json())
