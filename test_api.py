import httpx

BASE_URL = "http://127.0.0.1:8000"

def safe_request(method, url, **kwargs):
    try:
        response = httpx.request(method, url, timeout=10.0, **kwargs)
        response.raise_for_status()
        return response
    except httpx.HTTPStatusError as exc:
        print(f"❌ Error HTTP {exc.response.status_code}: {exc.response.text}")
    except Exception as e:
        print(f"❌ Error general: {e}")
    return None

def test_health_check():
    print("1️⃣ Health Check")
    r = safe_request("GET", f"{BASE_URL}/")
    if r: print(r.status_code, r.json())

def test_status_json():
    print("2️⃣ Status JSON")
    r = safe_request("GET", f"{BASE_URL}/status/json")
    if r: print(r.status_code, r.text)

def test_buscar_norma():
    print("3️⃣ Buscar Norma (dolo)")
    r = safe_request("GET", f"{BASE_URL}/legislacion/buscar", params={"palabra": "dolo"})
    if not r: return None
    print(r.status_code, r.text)
    try:
        data = r.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0]["id"]
        elif isinstance(data, dict) and "logs" in data and "output" in data["logs"]:
            output = data["logs"]["output"]
            return output.get("id") or 1234  # fallback
    except Exception as e:
        print("⚠️ Parsing error:", e)
    print("⚠️ No se encontró una norma válida.")
    return None

def test_obtener_norma(id_norma):
    print("4️⃣ Obtener Norma")
    r = safe_request("GET", f"{BASE_URL}/legislacion/norma/{id_norma}")
    if r: print(r.status_code, r.json())

def test_obtener_norma_bcn(id_norma):
    print("5️⃣ Obtener Norma BCN")
    r = safe_request("GET", f"{BASE_URL}/api/bcn/norma/{id_norma}")
    if r: print(r.status_code, r.json())

def test_reflexion():
    print("6️⃣ Reflexión Jurídica")
    payload = {
        "documento_analizado": "Este documento trata sobre la responsabilidad penal en el derecho chileno.",
        "criterios": ["culpabilidad", "dolo", "negligencia"]
    }
    r = safe_request("POST", f"{BASE_URL}/reflexion/", json=payload)
    if r: print(r.status_code, r.json())

def test_vision():
    print("7️⃣ Análisis de Imagen Legal")
    payload = {"image_id": "evidencia_2025_caso001.jpg"}
    r = safe_request("POST", f"{BASE_URL}/vision/", json=payload)
    if r: print(r.status_code, r.json())

def test_prediccion():
    print("8️⃣ Predicción Bayesiana")
    payload = {"contexto": "Una persona actúa con imprudencia al conducir, provocando daño a un peatón."}
    r = safe_request("POST", f"{BASE_URL}/api/prediccion/", json=payload)
    if r: print(r.status_code, r.json())

def test_predict():
    print("9️⃣ Experimento Predictivo General")
    payload = {"test": True}  # para evitar 400 vacío
    r = safe_request("POST", f"{BASE_URL}/predict", json=payload)
    if r: print(r.status_code, r.text)

if __name__ == "__main__":
    test_health_check()
    test_status_json()
    norma_id = test_buscar_norma()
    if norma_id:
        test_obtener_norma(norma_id)
        test_obtener_norma_bcn(norma_id)
    test_reflexion()
    test_vision()
    test_prediccion()
    test_predict()
