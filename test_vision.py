
import requests

API_URL = "http://127.0.0.1:10000/vision/"  # Cambiar si se despliega

def test_vision_endpoint():
    payload = {
        "image_id": "nombre_de_ejemplo.png"  # Asegúrate de que este archivo exista en /mnt/data/ si se prueba en servidor
    }
    response = requests.post(API_URL, json=payload)
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except Exception as e:
        print("Error en parseo JSON:", e)
        print("Texto crudo:", response.text)

if __name__ == "__main__":
    test_vision_endpoint()
