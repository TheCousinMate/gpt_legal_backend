#!/usr/bin/env python3
"""
Script de lanzamiento optimizado para Render
Forensic Legal Cognition 4.1
"""

import os
import sys
import logging
import uvicorn
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def setup_environment():
    """Configura el entorno de ejecución"""
    
    # Verificar archivos críticos
    critical_files = [
        "main.py",
        "utils_output.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in critical_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        logger.error(f"Archivos críticos faltantes: {missing_files}")
        sys.exit(1)
    
    # Verificar directorio modules
    if not Path("modules").exists():
        logger.error("Directorio 'modules' no encontrado")
        sys.exit(1)
    
    # Crear directorios si no existen
    Path("static").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    logger.info("Entorno configurado correctamente")

def get_port():
    """Obtiene el puerto desde variables de entorno"""
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Puerto configurado: {port}")
    return port

def get_host():
    """Obtiene el host para bind"""
    # En Render siempre usar 0.0.0.0
    host = "0.0.0.0"
    logger.info(f"Host configurado: {host}")
    return host

def main():
    """Función principal de lanzamiento"""
    logger.info("🚀 Iniciando Forensic Legal Cognition 4.1")
    
    try:
        # Configurar entorno
        setup_environment()
        
        # Obtener configuración
        host = get_host()
        port = get_port()
        
        # Configuración de uvicorn para producción
        config = {
            "app": "main:app",
            "host": host,
            "port": port,
            "workers": 1,  # Single worker en Render
            "loop": "auto",
            "http": "auto",
            "log_level": "info",
            "access_log": True,
            "use_colors": False,  # Mejor para logs en Render
            "reload": False,  # Nunca en producción
        }
        
        logger.info(f"Configuración uvicorn: {config}")
        logger.info("✅ Backend iniciando...")
        
        # Iniciar servidor
        uvicorn.run(**config)
        
    except KeyboardInterrupt:
        logger.info("🛑 Servidor detenido por usuario")
    except Exception as e:
        logger.error(f"❌ Error crítico al iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()