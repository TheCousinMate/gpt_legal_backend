#!/usr/bin/env python3
"""
Script de inicio para Forensic Legal Cognition 4.1
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_requirements():
    """Verifica que todos los archivos necesarios existan"""
    required_files = [
        "main.py",
        "router_universal.py", 
        "motor_predictivo.py",
        "utils_output.py",
        "requirements.txt",
        ".env",
        "band/matrix.jit",
        "modules/__init__.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Archivos faltantes:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ Todos los archivos necesarios están presentes")
    return True

def install_dependencies():
    """Instala las dependencias necesarias"""
    print("📦 Instalando dependencias...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencias instaladas correctamente")
            return True
        else:
            print(f"❌ Error instalando dependencias: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando pip: {e}")
        return False

def create_directories():
    """Crea directorios necesarios"""
    directories = [
        "band",
        "static",
        "static/.well-known",
        "modules",
        "logs",
        "models"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Directorio creado/verificado: {directory}")

def validate_matrix_config():
    """Valida la configuración de matrix.jit"""
    try:
        with open("band/matrix.jit", 'r') as f:
            config = json.load(f)
        
        required_keys = ["system_info", "status", "modules"]
        for key in required_keys:
            if key not in config:
                print(f"⚠️  Clave faltante en matrix.jit: {key}")
                return False
        
        print("✅ Configuración matrix.jit válida")
        return True
    except Exception as e:
        print(f"❌ Error validando matrix.jit: {e}")
        return False

def start_server():
    """Inicia el servidor FastAPI"""
    print("\n🚀 Iniciando servidor Forensic Legal Cognition 4.1...")
    print("📍 URL: http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/docs")
    print("🔍 Estado: http://localhost:8000/status")
    print("\n⏹️  Presiona Ctrl+C para detener el servidor\n")
    
    try:
        # Intenta usar el método preferido
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except ImportError:
        # Fallback a subprocess
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", 
                       "--host", "0.0.0.0", "--port", "8000", "--reload"])

def main():
    """Función principal"""
    print("🔍 Forensic Legal Cognition 4.1 - Inicializando...")
    print("=" * 60)
    
    # Verificar archivos
    if not check_requirements():
        print("\n❌ Faltan archivos necesarios. Revisa la estructura del proyecto.")
        return 1
    
    # Crear directorios
    create_directories()
    
    # Validar configuración
    if not validate_matrix_config():
        print("\n⚠️  Configuración incompleta pero continuando...")
    
    # Instalar dependencias
    if not install_dependencies():
        print("\n❌ Error instalando dependencias. Revisa requirements.txt")
        return 1
    
    # Iniciar servidor
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido por el usuario")
        return 0
    except Exception as e:
        print(f"\n❌ Error iniciando servidor: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)