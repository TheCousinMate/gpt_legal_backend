@echo off
echo 🔍 Validando static/openapi.yaml con Redocly CLI...
npx @redocly/cli lint static/openapi.yaml
pause
