
import streamlit as st
import requests
import json

st.set_page_config(page_title="Resolver IA · GPT Legal Backend · Visual Tester", layout="wide")
st.title("⚖️ Resolver IA · GPT Legal Backend · Visual Tester")

# Input de URL
backend_url = st.text_input("🔗 URL del backend:", "http://127.0.0.1:8000")

tabs = st.tabs(["/status/json", "/predict", "/reflexion", "/vision", "/bcn norma", "/legislacion buscar"])

# 1. /status/json
with tabs[0]:
    st.subheader("📊 Estado general del sistema /status/json")
    if st.button("📡 Verificar estado"):
        try:
            res = requests.get(f"{backend_url}/status/json")
            st.code(res.status_code)
            st.json(res.json())
        except Exception as e:
            st.error(f"Error: {e}")

# 2. /predict
with tabs[1]:
    st.subheader("🧠 Entrada legal para /predict")
    user_input = st.text_area("Texto legal o pregunta:")
    if st.button("🚀 Enviar a /predict"):
        try:
            res = requests.post(f"{backend_url}/predict", json={"input": user_input})
            st.code(res.status_code)
            st.json(res.json())
        except Exception as e:
            st.error(f"Error: {e}")

# 3. /reflexion
with tabs[2]:
    st.subheader("🔍 Reflexión Jurídica /reflexion/reflexion/")
    texto = st.text_area("Texto a analizar:")
    criterios = st.multiselect("Selecciona criterios:", ["legalidad", "proporcionalidad", "claridad", "consistencia"])
    if st.button("🧪 Enviar a /reflexion"):
        try:
            res = requests.post(f"{backend_url}/reflexion/reflexion/", json={"documento_analizado": texto, "criterios": criterios})
            st.code(res.status_code)
            st.json(res.json())
        except Exception as e:
            st.error(f"Error: {e}")

# 4. /vision
with tabs[3]:
    st.subheader("🖼️ Análisis visual /vision/vision/")
    image_id = st.text_input("ID de la imagen:")
    if st.button("📤 Enviar a /vision"):
        try:
            res = requests.post(f"{backend_url}/vision/vision/", json={"image_id": image_id})
            st.code(res.status_code)
            st.json(res.json())
        except Exception as e:
            st.error(f"Error: {e}")

# 5. /bcn norma
with tabs[4]:
    st.subheader("📘 Consulta BCN por ID /bcn/api/bcn/norma/{id}")
    norma_id = st.number_input("ID de norma BCN:", min_value=1, step=1)
    if st.button("🔎 Consultar norma BCN"):
        try:
            res = requests.get(f"{backend_url}/bcn/api/bcn/norma/{int(norma_id)}")
            st.code(res.status_code)
            st.json(res.json())
        except Exception as e:
            st.error(f"Error: {e}")

# 6. /legislacion buscar
with tabs[5]:
    st.subheader("📚 Búsqueda legislativa /legislacion/buscar?palabra=")
    palabra = st.text_input("Palabra clave:")
    if st.button("🔍 Buscar en legislación BCN"):
        try:
            res = requests.get(f"{backend_url}/legislacion/buscar", params={"palabra": palabra})
            st.code(res.status_code)
            st.json(res.json())
        except Exception as e:
            st.error(f"Error: {e}")
