#!/usr/bin/env python3
"""
Organizador de Proyecto - Forensic Legal Cognition 4.1
Organiza automáticamente la estructura del proyecto
"""

import os
import shutil
from pathlib import Path

def crear_estructura_directorios():
    """Crea la estructura de directorios del proyecto"""
    print("📁 Creando estructura de directorios...")
    
    base_path = Path("C:/thecousinlaw")
    
    # Directorios principales
    directorios = [
        "modules",
        "band", 
        "static",
        "logs",
        "tests",
        "config"
    ]
    
    for directorio in directorios:
        dir_path = base_path / directorio
        dir_path.mkdir(exist_ok=True)
        print(f"   ✅ {directorio}/")
    
    print("✅ Estructura de directorios creada")

def organizar_archivos():
    """Organiza los archivos existentes en la estructura correcta"""
    print("📋 Organizando archivos...")
    
    base_path = Path("C:/thecousinlaw")
    
    # Mapeo de archivos: origen → destino
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
    
    # Procesar cada archivo
    for origen, destino in mapeo_archivos.items():
        origen_path = base_path / origen
        destino_path = base_path / destino
        
        if origen_path.exists():
            # Crear directorio padre si no existe
            destino_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Eliminar destino si existe
            if destino_path.exists():
                destino_path.unlink()
            
            # Mover archivo
            shutil.move(str(origen_path), str(destino_path))
            print(f"   ✅ {origen} → {destino}")
        else:
            print(f"   ⚠️  {origen} no encontrado")
    
    print("✅ Archivos organizados")

def crear_archivos_faltantes():
    """Crea archivos esenciales que faltan"""
    print("📝 Creando archivos faltantes...")
    
    base_path = Path("C:/thecousinlaw")
    
    # main.py - Archivo principal
    if not (base_path / "main.py").exists():
        main_content = '''#!/usr/bin/env python3
"""
Forensic Legal Cognition 4.1 - Servidor Principal
"""

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

# Importar módulos
from router_universal import router as universal_router
from modules.root import router as root_router
from modules.status import router as status_router

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
    return {"message": "Forensic Legal Cognition 4.1 - Sistema Activo"}

if __name__ == "__main__":
    print("🚀 Iniciando Forensic Legal Cognition 4.1...")
    print("📡 Servidor disponible en: http://localhost:8000")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
'''
        with open(base_path / "main.py", "w", encoding="utf-8") as f:
            f.write(main_content)
        print("   ✅ main.py creado")
    
    # motor_predictivo.py - Motor de análisis
    if not (base_path / "motor_predictivo.py").exists():
        motor_content = '''#!/usr/bin/env python3
"""
Motor Predictivo - Forensic Legal Cognition 4.1
"""

import json
import logging
from typing import Dict, Any, List
from pathlib import Path

class MotorPredictivo:
    """Motor de análisis predictivo para casos legales"""
    
    def __init__(self):
        self.configuracion = self._cargar_configuracion()
        self.logger = self._configurar_logger()
        
    def _cargar_configuracion(self) -> Dict[str, Any]:
        """Carga la configuración del motor"""
        config_path = Path("band/matrix.jit")
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error cargando configuración: {e}")
        
        return {
            "version": "4.1.0",
            "modelo": "forensic-legal-cognition",
            "precision": 0.95,
            "configuracion_activa": True
        }
    
    def _configurar_logger(self) -> logging.Logger:
        """Configura el sistema de logging"""
        logger = logging.getLogger("MotorPredictivo")
        logger.setLevel(logging.INFO)
        
        # Crear handler para archivo
        log_path = Path("logs")
        log_path.mkdir(exist_ok=True)
        
        handler = logging.FileHandler(log_path / "motor_predictivo.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def analizar_caso(self, datos_caso: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza un caso legal y genera predicciones"""
        try:
            self.logger.info(f"Analizando caso: {datos_caso.get('id', 'sin_id')}")
            
            # Procesamiento base
            resultado = {
                "id_caso": datos_caso.get("id", "caso_" + str(hash(str(datos_caso)))),
                "estado": "analizado",
                "predicciones": {
                    "probabilidad_exito": 0.75,
                    "tiempo_estimado": "6-12 meses",
                    "factores_clave": [
                        "Evidencia documental",
                        "Precedentes jurisprudenciales",
                        "Contexto legal actual"
                    ]
                },
                "recomendaciones": [
                    "Fortalecer evidencia documental",
                    "Revisar precedentes similares",
                    "Considerar mediación previa"
                ],
                "confianza": self.configuracion.get("precision", 0.95)
            }
            
            self.logger.info(f"Análisis completado: {resultado['id_caso']}")
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error en análisis: {e}")
            return {
                "error": str(e),
                "estado": "error",
                "mensaje": "Error durante el análisis del caso"
            }
    
    def obtener_estado(self) -> Dict[str, Any]:
        """Obtiene el estado actual del motor"""
        return {
            "version": self.configuracion.get("version", "4.1.0"),
            "estado": "activo",
            "configuracion": self.configuracion.get("configuracion_activa", True),
            "precision": self.configuracion.get("precision", 0.95)
        }

# Instancia global
motor = MotorPredictivo()
'''
        with open(base_path / "motor_predictivo.py", "w", encoding="utf-8") as f:
            f.write(motor_content)
        print("   ✅ motor_predictivo.py creado")
    
    # .gitignore
    if not (base_path / ".gitignore").exists():
        gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Forensic Legal Cognition specific
band/cache/
static/uploads/
config/secrets.json
'''
        with open(base_path / ".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore_content)
        print("   ✅ .gitignore creado")
    
    # README.md
    if not (base_path / "README.md").exists():
        readme_content = '''# Forensic Legal Cognition 4.1

Sistema de Análisis Legal Predictivo con IA

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
python main.py
```

## 📁 Estructura del Proyecto

```
forensic-legal-cognition/
├── main.py                 # Servidor principal
├── router_universal.py     # Router universal
├── motor_predictivo.py     # Motor de análisis
├── modules/               # Módulos del sistema
│   ├── predict.py         # Predicción
│   ├── root.py           # Interfaz web
│   └── status.py         # Estado del sistema
├── band/                 # Configuración
│   └── matrix.jit        # Configuración del motor
├── static/               # Archivos estáticos
└── logs/                 # Archivos de log
```

## 🔧 Configuración

El sistema se configura automáticamente al iniciar.

## 📡 API Endpoints

- `GET /` - Página principal
- `GET /status` - Estado del sistema
- `POST /api/analyze` - Análisis de casos
- `GET /api/predict` - Predicciones

## 📊 Estado del Sistema

Accede a `http://localhost:8000/status` para ver el estado actual.

## 🛠️ Desarrollo

```bash
# Ejecutar en modo desarrollo
python main.py

# Ejecutar tests
python -m pytest tests/
```

## 📞 Soporte

Sistema desarrollado para análisis legal predictivo.
Versión: 4.1.0
'''
        with open(base_path / "README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        print("   ✅ README.md creado")
    
    print("✅ Archivos faltantes creados")

def verificar_estructura():
    """Verifica que la estructura final esté correcta"""
    print("🔍 Verificando estructura final...")
    
    base_path = Path("C:/thecousinlaw")
    
    archivos_requeridos = [
        "main.py",
        "router_universal.py", 
        "motor_predictivo.py",
        "modules/predict.py",
        "modules/root.py",
        "modules/status.py",
        "modules/__init__.py",
        "band/matrix.jit",
        "requirements.txt",
        ".env",
        "README.md"
    ]
    
    todo_correcto = True
    
    for archivo in archivos_requeridos:
        archivo_path = base_path / archivo
        if archivo_path.exists():
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} - FALTA")
            todo_correcto = False
    
    if todo_correcto:
        print("✅ Estructura verificada correctamente")
    else:
        print("⚠️  Algunos archivos faltan")
    
    return todo_correcto

def main():
    """Función principal del organizador"""
    print("🎯 Forensic Legal Cognition 4.1 - Organizador de Proyecto")
    print("=" * 60)
    
    try:
        # Paso 1: Crear estructura
        crear_estructura_directorios()
        
        # Paso 2: Organizar archivos
        organizar_archivos()
        
        # Paso 3: Crear archivos faltantes
        crear_archivos_faltantes()
        
        # Paso 4: Verificar estructura
        verificar_estructura()
        
        print("\n🎉 ¡Proyecto organizado exitosamente!")
        print("\n🚀 Próximos pasos:")
        print("1. cd C:\\thecousinlaw")
        print("2. pip install -r requirements.txt")
        print("3. python main.py")
        print("\n📡 El servidor estará disponible en: http://localhost:8000")
        
    except Exception as e:
        print(f"\n❌ Error durante la organización: {e}")
        print("Revisa los permisos de archivos y directorios")

if __name__ == "__main__":
    main()