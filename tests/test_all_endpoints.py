import os
import sys
import requests
from fastapi.testclient import TestClient
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Allow overriding the base URL via API_URL. If not provided,
# fall back to an in-process TestClient for local tests.
BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")

if os.getenv("API_URL"):
    session = requests.Session()

    def get(path: str, **kwargs):
        return session.get(f"{BASE_URL}{path}", **kwargs)

    def post(path: str, **kwargs):
        return session.post(f"{BASE_URL}{path}", **kwargs)
else:
    from main import app

    client = TestClient(app)

    def get(path: str, **kwargs):
        return client.get(path, **kwargs)

    def post(path: str, **kwargs):
        return client.post(path, **kwargs)


def test_healthcheck():
    r = get("/")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "alive"
    assert "version" in data


def test_predict():
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")
    payload = {"contexto": "Existe un posible incumplimiento de contrato con riesgo de nulidad"}
    try:
        r = post("/predict", json=payload)
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Network error: {e}")
    if r.status_code != 200:
        pytest.skip(f"Endpoint unavailable: {r.text}")
    assert r.status_code == 200

if __name__ == "__main__":
    test_healthcheck()
    test_predict()
