# Forensic Legal Cognition 4.1 — Backend Privado

Este repositorio contiene una arquitectura legal forense desarrollada en colaboración con el entorno GPT mediante interacción conversacional directa, basada en más de 50 millones de tokens validados, sin exposición pública de sus capas internas ni de sus módulos críticos.

🔒 Repositorio privado  
📜 Modelo registrado con licencia SafeCreative  
🧠 Entrenado conversacionalmente (sept. 2023 — mayo 2025)  
🚫 No exponer estructura, endpoints ni funciones del backend

Todos los derechos reservados. Uso exclusivo por Kabir K. Hazbún Crovetto.

## Pruebas

Los tests funcionan de forma local usando `TestClient`, por lo que no es necesario
levantar el servidor. Ejecuta simplemente:

```bash
pytest -q
```

Si quieres probar contra un backend desplegado, establece `API_URL` con la URL
base del servicio y los tests enviarán las peticiones reales:

```bash
API_URL=https://tubackend.example.com pytest -q
```

The `/predict` endpoint relies on the OpenAI API. Provide your key via the
`OPENAI_API_KEY` environment variable when running the backend or the tests:

```bash
OPENAI_API_KEY=sk-... uvicorn main:app --reload
```
