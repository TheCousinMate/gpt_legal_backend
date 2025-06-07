
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

@patch("openai.ChatCompletion.create", side_effect=dummy_chatcompletion_create)
def test_reflexion(mock_create):
    payload = {"contexto": "El contrato fue firmado solo por una parte"}
    r = client.post("/reflexion", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["reflexion"] == "mock response"

@patch("openai.ChatCompletion.create", side_effect=dummy_chatcompletion_create)
def test_interpretar(mock_create):
    payload = {"contexto": "¿Puede un menor firmar un contrato en Chile?"}
    r = client.post("/interpretar", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["respuesta"] == "mock response"

@patch("openai.ChatCompletion.create", side_effect=dummy_chatcompletion_create)
def test_vision(mock_create):
    payload = {"contexto": "https://example.com/fakeimage.png"}
    r = client.post("/vision", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["descripcion"] == "mock response"
