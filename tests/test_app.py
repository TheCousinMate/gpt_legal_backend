
from fastapi.testclient import TestClient
from unittest.mock import patch
import openai
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import main

client = TestClient(main.app)

class DummyResp:
    def __init__(self, content="mock response"):
        self.choices = [type("obj", (), {"message": {"content": content}})()]

def dummy_chatcompletion_create(*args, **kwargs):
    return DummyResp()

def test_healthcheck():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "alive"
    assert "version" in data

@patch("openai.ChatCompletion.create", side_effect=dummy_chatcompletion_create)
def test_predict(mock_create):
    payload = {"contexto": "Existe un posible incumplimiento de contrato con riesgo de nulidad"}
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["resultado"] == "mock response"
