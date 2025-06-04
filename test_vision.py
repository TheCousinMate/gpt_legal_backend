import os
import io
import sys
import shutil
import requests
from fastapi.testclient import TestClient
from PIL import Image
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

API_URL = os.getenv("API_URL")

if API_URL:
    def post_file(files):
        return requests.post(f"{API_URL.rstrip('/')}/vision", files=files)
else:
    from main import app

    client = TestClient(app)

    def post_file(files):
        return client.post("/vision", files=files)

tesseract_available = shutil.which("tesseract") is not None

@pytest.mark.skipif(not tesseract_available and not API_URL, reason="tesseract not installed")
def test_vision_endpoint():
    image = Image.new("RGB", (100, 100), color=(255, 255, 255))
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    files = {"file": ("test.png", buf, "image/png")}
    response = post_file(files)
    assert response.status_code in (200, 422)

if __name__ == "__main__":
    test_vision_endpoint()
