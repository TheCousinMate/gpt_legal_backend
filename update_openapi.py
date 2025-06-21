from main import app
import json
with open("static/openapi.json", "w", encoding="utf-8") as f:
    json.dump(app.openapi(), f, indent=2, ensure_ascii=False)
