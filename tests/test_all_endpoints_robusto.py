
import requests
import json

BASE = "http://127.0.0.1:8000"

def safe_call(name, func):
    print(f"\n[✔] {name}")
    try:
        func()
    except Exception as e:
        print(f"[✘] Error en {name}: {str(e)}")

def check_status():
    r = requests.get(f"{BASE}/status/json")
    print("Status:", r.status_code)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def check_predict():
    r = requests.post(f"{BASE}/predict", json={
        "input": "¿Puede una empresa despedir a un trabajador sin causa justificada ni indemnización?"
    })
    print("Status:", r.status_code)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def check_reflexion():
    r = requests.post(f"{BASE}/reflexion/reflexion/", json={
        "documento_analizado": "El empleador puede exigir horas extra sin acuerdo del trabajador.",
        "criterios": ["legalidad", "proporcionalidad"]
    })
    print("Status:", r.status_code)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def check_vision():
    r = requests.post(f"{BASE}/vision/vision/", json={"image_id": "demo_123_firma"})
    print("Status:", r.status_code)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def check_bcn():
    r = requests.get(f"{BASE}/bcn/api/bcn/norma/18046")
    print("Status:", r.status_code)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def check_busqueda():
    r = requests.get(f"{BASE}/legislacion/buscar", params={"palabra": "contrato"})
    print("Status:", r.status_code)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def main():
    safe_call("/status/json", check_status)
    safe_call("/predict", check_predict)
    safe_call("/reflexion/reflexion/", check_reflexion)
    safe_call("/vision/vision/", check_vision)
    safe_call("/bcn/api/bcn/norma/18046", check_bcn)
    safe_call("/legislacion/buscar", check_busqueda)

if __name__ == "__main__":
    main()
