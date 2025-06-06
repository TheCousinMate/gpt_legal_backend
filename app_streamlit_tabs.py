# app_streamlit_tabs.py

import streamlit as st
import requests

API_BASE = "https://gpt-legal-backend.onrender.com"

st.set_page_config(page_title="Legal Cognition 4.1", layout="wide")
st.title("⚖️ Legal Cognition Interface")

opcion = st.sidebar.selectbox("Elige módulo:", ["Reflexión", "Predicción", "Predict"], index=0)

if opcion == "Reflexión":
    st.header("📘 Reflexión Jurídica Automatizada")
    texto = st.text_area("Texto normativo o doctrinal:")
    criterios = st.text_input("Criterios separados por coma:")
    if st.button("Analizar"):
        r = requests.post(f"{API_BASE}/reflexion/", json={
            "documento_analizado": texto,
            "criterios": [c.strip() for c in criterios.split(",") if c.strip()]
        })
        st.write(r.json())

elif opcion == "Predicción":
    st.header("🔮 Riesgo Legal Predictivo")
    contexto = st.text_area("Describe el contexto legal a evaluar:")
    if st.button("Predecir riesgo"):
        r = requests.post(f"{API_BASE}/api/prediccion/", json={"contexto": contexto})
        st.write(r.json())

elif opcion == "Predict":
    st.header("🧪 Predict API (Experimental)")
    if st.button("Test Predict"):
        r = requests.post(f"{API_BASE}/predict", json={"test": True})
        st.write(r.text)
