import pytest
import requests

API_URL = "https://gpt-legal-backend-bodukoeg-thecousinmates-projects.vercel.app/vision/"

pytest.skip("External vision endpoint not available in test environment", allow_module_level=True)

def test_vision_endpoint():
    payload = {
        "image_id": "ejemplo.png"  # Asegúrate de que este archivo esté en /mnt/data o accesible si es servidor real
    }
    response = requests.post(API_URL, json=payload)
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except Exception as e:
        print("❌ Error en parseo JSON:", e)
        print("Texto crudo:", response.text)

if __name__ == "__main__":
    test_vision_endpoint()
