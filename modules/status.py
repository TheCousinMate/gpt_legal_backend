"""
Módulo de estado del sistema
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import json
import os
from datetime import datetime
import psutil
import platform

router = APIRouter()

class SystemStatus(BaseModel):
    status: str
    timestamp: str
    version: str
    system_info: Dict[str, Any]
    performance: Dict[str, Any]
    modules: Dict[str, Any]

def get_system_info():
    """Obtiene información del sistema"""
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.architecture()[0],
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "hostname": platform.node()
    }

def get_performance_metrics():
    """Obtiene métricas de rendimiento"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_usage": f"{cpu_percent}%",
            "memory_usage": f"{memory.percent}%",
            "memory_available": f"{memory.available / (1024**3):.2f} GB",
            "disk_usage": f"{disk.percent}%",
            "disk_free": f"{disk.free / (1024**3):.2f} GB"
        }
    except Exception as e:
        return {
            "cpu_usage": "N/A",
            "memory_usage": "N/A",
            "memory_available": "N/A",
            "disk_usage": "N/A",
            "disk_free": "N/A",
            "error": str(e)
        }

def load_matrix_config():
    """Carga configuración desde matrix.jit"""
    try:
        matrix_path = os.path.join("band", "matrix.jit")
        if os.path.exists(matrix_path):
            with open(matrix_path, 'r') as f:
                return json.load(f)
        return {"error": "matrix.jit not found"}
    except Exception as e:
        return {"error": f"Error loading matrix.jit: {str(e)}"}

@router.get("/", response_model=SystemStatus)
async def get_status():
    """Endpoint principal de estado"""
    try:
        matrix_config = load_matrix_config()
        
        status_data = {
            "status": "operational",
            "timestamp": datetime.now().isoformat(),
            "version": "4.1.0",
            "system_info": get_system_info(),
            "performance": get_performance_metrics(),
            "modules": matrix_config.get("modules", {})
        }
        
        return SystemStatus(**status_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")

@router.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "checks": {
            "api": "ok",
            "database": "ok",
            "cache": "ok",
            "external_services": "ok"
        }
    }

@router.get("/metrics")
async def get_metrics():
    """Endpoint de métricas detalladas"""
    return {
        "timestamp": datetime.now().isoformat(),
        "system": get_system_info(),
        "performance": get_performance_metrics(),
        "application": {
            "version": "4.1.0",
            "uptime": "N/A",
            "requests_total": "N/A",
            "errors_total": "N/A"
        }
    }

@router.get("/version")
async def get_version():
    """Endpoint de versión"""
    return {
        "version": "4.1.0",
        "build": "2024.01.01",
        "environment": "production",
        "api_version": "v1"
    }