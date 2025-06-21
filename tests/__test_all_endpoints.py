import requests

BASE_URL = "http://127.0.0.1:10000"

def test_healthcheck():
    url = f"{BASE_URL}/"
    r = requests.get(url)
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "alive"
    assert "version" in data
    print("[OK] Healthcheck passed")

def test_predict():
    url = f"{BASE_URL}/predict"
    payload = {"contexto": "Existe un posible incumplimiento de contrato con riesgo de nulidad"}
    r = requests.post(url, json=payload)
    assert r.status_code == 200, f"Status code {r.status_code}, response: {r.text}"
    print("[OK] Predict endpoint passed")

if __name__ == "__main__":
    test_healthcheck()
    test_predict()
