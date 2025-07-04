#!/usr/bin/env python3
"""
Script de inicio rápido para Forensic Legal Cognition 4.1
Ejecuta organización y luego inicia el servidor
"""

import os
import sys
import subprocess
from pathlib import Path

def ejecutar_organizacion():
    """Ejecuta el organizador del proyecto"""
    print("🔧 Organizando proyecto...")
    
    # Código del organizador integrado
    from pathlib import Path
    import shutil
    
    base_path = Path("C:/thecousinlaw")
    
    # Mapeo de archivos
    archivos_existentes = {
        "predict_corregido.py": "modules/predict.py",
        "router_universal_corregido.py": "router_universal.py",
        "startup_script.py": "start.py",
        "root_module.py": "modules/root.py",
        "status_module.py": "modules/status.py",
        "matrix_jit.json": "band/matrix.jit",
        "modules_init.py": "modules/__init__.py",
        "env_config (1).sh": ".env",
        "requirements_txt.txt": "requirements.txt"
    }
    
    # Crear directorios
    directorios = ["modules", "band", "static", "logs"]
    for dir_name in directorios:
        (base_path / dir_name).mkdir(exist_ok=True)
    
    # Mover archivos
    for origen, destino in archivos_existentes.items():
        origen_path = base_path / origen
        destino_path = base_path / destino
        
        if origen_path.exists():
            destino_path.parent.mkdir(parents=True, exist_ok=True)
            if destino_path.exists():
                destino_path.unlink()
            shutil.move(str(origen_path), str(destino_path))
            print(f"   ✅ {origen} → {destino}")
    
    print("✅ Organización completada")

def verificar_dependencias():
    """Verifica e instala dependencias"""
    print("📦 Verificando dependencias...")
    
    try:
        # Verificar si requirements.txt existe
        if Path("requirements.txt").exists():
            print("   Instalando dependencias...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True, capture_output=True)
            print("   ✅ Dependencias instaladas")
        else:
            print("   ⚠️  requirements.txt no encontrado, instalando paquetes básicos...")
            paquetes = ["fastapi", "uvicorn", "transformers", "torch", "python-dotenv"]
            for paquete in paquetes:
                subprocess.run([sys.executable, "-m", "pip", "install", paquete], 
                             check=True, capture_output=True)
            print("   ✅ Paquetes básicos instalados")
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️  Error instalando dependencias: {e}")

def iniciar_servidor():
    """Inicia el servidor FastAPI"""
    print("🚀 Iniciando servidor...")
    
    try:
        # Cambiar al directorio del proyecto
        os.chdir("C:/thecousinlaw")
        
        # Verificar que main.py existe
        if not Path("main.py").exists():
            print("❌ main.py no encontrado")
            return False
        
        # Iniciar servidor
        print("   Servidor iniciando en http://localhost:8000")
        print("   Presiona Ctrl+C para detener")
        
        subprocess.run([sys.executable, "main.py"], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error iniciando servidor: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    
    return True

def main():
    """Función principal"""
    print("🎯 Forensic Legal Cognition 4.1 - Inicio Rápido")
    print("=" * 50)
    
    try:
        # Paso 1: Organizar proyecto
        ejecutar_organizacion()
        
        # Paso 2: Verificar dependencias
        verificar_dependencias()
        
        # Paso 3: Iniciar servidor
        iniciar_servidor()
        
    except Exception as e:
        print(f"❌ Error durante el inicio: {e}")
        print("\n🔧 Pasos manuales:")
        print("1. Ejecutar: python organizar_proyecto.py")
        print("2. Ejecutar: pip install -r requirements.txt")
        print("3. Ejecutar: python main.py")

if __name__ == "__main__":
    main()
