#!/usr/bin/env python3
"""
Script de Inicio Rápido - Forensic Legal Cognition 4.1
Organiza el proyecto e inicia el servidor automáticamente
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def organizar_proyecto():
    """Organiza automáticamente el proyecto"""
    print("🔧 Organizando proyecto...")
    
    base_path = Path("C:/thecousinlaw")
    
    # Crear directorios
    directorios = ["modules", "band", "static", "logs", "tests", "config"]
    for directorio in directorios:
        (base_path / directorio).mkdir(exist_ok=True)
    
    # Mapeo de archivos
    mapeo_archivos = {
        "predict_corregido.py": "modules/predict.py",
        "router_universal_corregido.py": "router_universal.py",
        "startup_script.py": "start.py",
        "root_module.py": "modules/root.py",
        "status_module.py": "modules/status.py",
        "matrix_jit.json": "band/matrix.jit",
        "modules_init.py": "modules/__init__.py",
        "env_config (1).sh": ".env",
        "requirements_txt.txt": "requirements.txt",
        "utils_output.py": "utils_output.py"
    }
    
    # Procesar archivos
    for origen, destino in mapeo_archivos.items():
        origen_path = base_path / origen
        destino_path = base_path / destino
        
        if origen_path.exists():
            destino_path.parent.mkdir(parents=True, exist_ok=True)
            if destino_path.exists():
                destino_path.unlink()
            shutil.move(str(origen_path), str(destino_path))
            print(f"   ✅ {origen} → {destino}")
    
    # Crear main.py si no existe
    if not (base_path / "main.py").exists():
        main_content = '''#!/usr/bin/env python3
"""
Forensic Legal Cognition 4.1 - Servidor Principal
"""

try:
    import uvicorn
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
    from pathlib import Path
    import os
    
    # Importar módulos locales
    try:
        from router_universal import router as universal_router
    except ImportError:
        print("⚠️  router_universal no encontrado, creando router básico...")
        from fastapi import APIRouter
        universal_router = APIRouter()
        
        @universal_router.get("/analyze")
        async def analyze():
            return {"message": "Análisis disponible", "status": "ready"}
    
    try:
        from modules.root import router as root_router
    except ImportError:
        print("⚠️  modules.root no encontrado, creando router básico...")
        from fastapi import APIRouter
        root_router = APIRouter()
        
        @root_router.get("/")
        async def root():
            return {"message": "Forensic Legal Cognition 4.1 - Sistema Activo"}
    
    try:
        from modules.status import router as status_router
    except ImportError:
        print("⚠️  modules.status no encontrado, creando router básico...")
        from fastapi import APIRouter
        status_router = APIRouter()
        
        @status_router.get("/")
        async def status():
            return {"status": "active", "version": "4.1.0"}
    
    # Crear aplicación FastAPI
    app = FastAPI(
        title="Forensic Legal Cognition 4.1",
        description="Sistema de Análisis Legal Predictivo",
        version="4.1.0"
    )
    
    # Configurar archivos estáticos
    if Path("static").exists():
        app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Registrar routers
    app.include_router(universal_router, prefix="/api")
    app.include_router(root_router, prefix="/")
    app.include_router(status_router, prefix="/status")
    
    @app.get("/")
    async def root():
        return {
            "message": "Forensic Legal Cognition 4.1 - Sistema Activo",
            "version": "4.1.0",
            "status": "operational",
            "endpoints": {
                "main": "/",
                "status": "/status",
                "api": "/api",
                "analyze": "/api/analyze"
            }
        }
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "timestamp": "2025-07-04"}
    
    if __name__ == "__main__":
        print("🚀 Iniciando Forensic Legal Cognition 4.1...")
        print("📡 Servidor disponible en: http://localhost:8000")
        print("🔗 Endpoints disponibles:")
        print("   - GET / (página principal)")
        print("   - GET /health (estado de salud)")
        print("   - GET /status (estado del sistema)")
        print("   - GET /api/analyze (análisis)")
        print("\\n⚡ Presiona Ctrl+C para detener")
        
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )

except ImportError as e:
    print(f"❌ Error importando dependencias: {e}")
    print("💡 Instalando dependencias necesarias...")
    import subprocess
    import sys
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", 
                       "fastapi", "uvicorn", "python-multipart"], 
                      check=True)
        print("✅ Dependencias instaladas, reinicia el servidor")
    except subprocess.CalledProcessError:
        print("❌ Error instalando dependencias")
        print("🔧 Instala manualmente: pip install fastapi uvicorn")
        
except Exception as e:
    print(f"❌ Error general: {e}")
    print("🔧 Verifica la configuración del proyecto")
'''
        with open(base_path / "main.py", "w", encoding="utf-8") as f:
            f.write(main_content)
        print("   ✅ main.py creado")
    
    print("✅ Proyecto organizado")

def instalar_dependencias():
    """Instala dependencias necesarias"""
    print("📦 Instalando dependencias...")
    
    try:
        # Dependencias básicas
        dependencias = [
            "fastapi",
            "uvicorn[standard]",
            "python-multipart",
            "python-dotenv",
            "pathlib"
        ]
        
        for dep in dependencias:
            print(f"   Instalando {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                          check=True, capture_output=True)
        
        print("✅ Dependencias instaladas")
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Error instalando algunas dependencias: {e}")
        print("💡 Continuando con las dependencias disponibles...")

def verificar_archivos():
    """Verifica que los archivos principales existan"""
    print("🔍 Verificando archivos...")
    
    base_path = Path("C:/thecousinlaw")
    archivos_esenciales = ["main.py"]
    
    for archivo in archivos_esenciales:
        if (base_path / archivo).exists():
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} - FALTA")
            return False
    
    return True

def iniciar_servidor():
    """Inicia el servidor"""
    print("🚀 Iniciando servidor...")
    
    try:
        # Cambiar al directorio del proyecto
        os.chdir("C:/thecousinlaw")
        
        print("📡 Servidor iniciando en http://localhost:8000")
        print("🔗 Endpoints disponibles:")
        print("   - GET / (página principal)")
        print("   - GET /health (estado de salud)")
        print("   - GET /status (estado del sistema)")
        print("   - GET /api/analyze (análisis)")
        print("\\n⚡ Presiona Ctrl+C para detener")
        
        # Ejecutar el servidor
        subprocess.run([sys.executable, "main.py"], check=True)
        
    except KeyboardInterrupt:
        print("\\n🛑 Servidor detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando el servidor: {e}")
        print("🔧 Intenta ejecutar manualmente: python main.py")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def main():
    """Función principal - TODO EN UNO"""
    print("🎯 Forensic Legal Cognition 4.1 - Inicio Rápido")
    print("=" * 60)
    
    try:
        # Paso 1: Organizar proyecto
        organizar_proyecto()
        
        # Paso 2: Instalar dependencias
        instalar_dependencias()
        
        # Paso 3: Verificar archivos
        if not verificar_archivos():
            print("❌ Archivos faltantes, abortando...")
            return
        
        # Paso 4: Iniciar servidor
        iniciar_servidor()
        
    except Exception as e:
        print(f"❌ Error durante el inicio: {e}")
        print("\\n🔧 Pasos manuales:")
        print("1. cd C:\\thecousinlaw")
        print("2. pip install fastapi uvicorn")
        print("3. python main.py")

if __name__ == "__main__":
    main()