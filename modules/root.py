"""
Módulo raíz del sistema - Endpoint principal
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Dict, Any
import json
import os
from datetime import datetime

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root():
    """Endpoint raíz del sistema"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Forensic Legal Cognition 4.1</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
            .endpoint { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { background: #3498db; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px; margin-right: 10px; }
            .status { color: #27ae60; font-weight: bold; }
            .version { color: #8e44ad; font-style: italic; }
            a { color: #3498db; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
            .card { background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #3498db; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Forensic Legal Cognition 4.1</h1>
            <p class="status">Sistema Operativo</p>
            <p class="version">Versión 4.1.0 - Build 2024.01.01</p>
            
            <div class="grid">
                <div class="card">
                    <h3>📊 Análisis Predictivo</h3>
                    <p>Motor de análisis legal con IA avanzada</p>
                    <a href="/predict">Acceder al endpoint</a>
                </div>
                
                <div class="card">
                    <h3>🏛️ Corpus Legal</h3>
                    <p>Base de conocimiento jurídico especializado</p>
                    <a href="/corpus">Explorar corpus</a>
                </div>
                
                <div class="card">
                    <h3>🔬 Visión Forense</h3>
                    <p>Análisis avanzado de evidencias</p>
                    <a href="/vision">Análisis forense</a>
                </div>
                
                <div class="card">
                    <h3>📈 Predicción Bayesiana</h3>
                    <p>Modelos probabilísticos especializados</p>
                    <a href="/bayesian">Análisis bayesiano</a>
                </div>
            </div>
            
            <h2>🔗 Endpoints Disponibles</h2>
            
            <div class="endpoint">
                <span class="method">POST</span><strong>/predict</strong> - Análisis legal predictivo
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span><strong>/status</strong> - Estado del sistema
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span><strong>/reflexion</strong> - Análisis reflexivo
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span><strong>/vision</strong> - Análisis forense visual
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span><strong>/legislacion</strong> - Legislación BCN
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span><strong>/corpus</strong> - Corpus legal
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span><strong>/bayesian</strong> - Predicción bayesiana
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span><strong>/interprete</strong> - Intérprete legal
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span><strong>/diagnostico</strong> - Diagnóstico del sistema
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span><strong>/docs</strong> - Documentación interactiva
            </div>
            
            <h2>📋 Información del Sistema</h2>
            <p><strong>Última actualización:</strong> """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            <p><strong>Arquitectura:</strong> FastAPI + Transformers + PyTorch</p>
            <p><strong>Funcionalidades:</strong> Análisis legal, predicción, corpus jurídico, visión forense</p>
            
            <hr>
            <p style="text-align: center; color: #7f8c8d; font-size: 14px;">
                © 2024 Forensic Legal Cognition - Sistema de Análisis Legal Avanzado
            </p>
        </div>
    </body>
    </html>
    """
    return html_content

@router.get("/info")
async def get_info():
    """Información básica del sistema"""
    return {
        "system": "Forensic Legal Cognition",
        "version": "4.1.0",
        "description": "Sistema de análisis legal avanzado con IA",
        "endpoints": [
            "/predict",
            "/status", 
            "/reflexion",
            "/vision",
            "/legislacion",
            "/corpus",
            "/bayesian",
            "/interprete",
            "/diagnostico"
        ],
        "features": [
            "Análisis predictivo legal",
            "Corpus jurídico especializado",
            "Visión forense avanzada",
            "Predicción bayesiana",
            "Intérprete legal automático"
        ],
        "timestamp": datetime.now().isoformat()
    }

@router.get("/welcome")
async def welcome():
    """Mensaje de bienvenida"""
    return {
        "message": "Bienvenido a Forensic Legal Cognition 4.1",
        "description": "Sistema de análisis legal avanzado con inteligencia artificial",
        "status": "Operativo",
        "next_steps": [
            "Explorar endpoints disponibles",
            "Revisar documentación en /docs",
            "Probar análisis predictivo en /predict",
            "Verificar estado del sistema en /status"
        ]
    }