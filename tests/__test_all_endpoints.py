import requests

BASE = "http://127.0.0.1:8000"

def check(endpoint, method='get', data=None, params=None):
    try:
        if method == 'get':
            r = requests.get(BASE + endpoint, params=params)
        else:
            r = requests.post(BASE + endpoint, json=data)
        r.raise_for_status()
        print(f"✅ {endpoint} OK")
    except Exception as e:
        print(f"❌ {endpoint} FALLÓ: {e}")

check("/")
check("/reflexion/", 'post', {"documento_analizado": "Ley chilena...", "criterios": ["claridad"]})
check("/vision/", 'post', {"image_id": "imagen123"})
check("/forensics/search", 'get', None, {"pregunta": "Derechos del consumidor"})
check("/legislacion/buscar", 'get', None, {"palabra": "contrato"})
