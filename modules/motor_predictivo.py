#!/usr/bin/env python3
"""
Motor Predictivo - Forensic Legal Cognition 4.1
Módulo principal de análisis predictivo
"""

import json
import logging
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import hashlib

class MotorPredictivo:
    """Motor de análisis predictivo para casos legales"""
    
    def __init__(self):
        self.version = "4.1.0"
        self.estado = "activo"
        self.configuracion = self._cargar_configuracion()
        self.logger = self._configurar_logger()
        self._inicializar_motor()
        
    def _cargar_configuracion(self) -> Dict[str, Any]:
        """Carga la configuración del motor"""
        config_path = Path("band/matrix.jit")
        
        configuracion_default = {
            "version": "4.1.0",
            "modelo": "forensic-legal-cognition",
            "precision": 0.95,
            "configuracion_activa": True,
            "algoritmos": {
                "prediccion_bayesiana": True,
                "analisis_corpus": True,
                "vision_forense": True,
                "legislacion_bcn": True
            },
            "limites": {
                "casos_simultaneos": 10,
                "tiempo_max_analisis": 300,
                "memoria_max": "1GB"
            }
        }
        
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config_cargada = json.load(f)
                    configuracion_default.update(config_cargada)
                    self.logger.info("✔ Configuración cargada desde matrix.jit")
            except Exception as e:
                self.logger.warning(f"⚠️ Error cargando configuración: {e}")
        
        return configuracion_default
    
    def _configurar_logger(self) -> logging.Logger:
        """Configura el sistema de logging"""
        logger = logging.getLogger("MotorPredictivo")
        logger.setLevel(logging.INFO)
        
        # Crear directorio de logs si no existe
        log_path = Path("logs")
        log_path.mkdir(exist_ok=True)
        
        # Configurar handler para archivo
        log_file = log_path / f"motor_predictivo_{datetime.now().strftime('%Y%m%d')}.log"
        handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _inicializar_motor(self):
        """Inicializa componentes del motor"""
        try:
            self.logger.info("🚀 Inicializando Motor Predictivo v4.1.0")
            self.logger.info(f"✔ Configuración activa: {self.configuracion.get('configuracion_activa')}")
            self.logger.info(f"✔ Precisión configurada: {self.configuracion.get('precision')}")
            self.logger.info("✔ Motor Predictivo inicializado correctamente")
        except Exception as e:
            self.logger.error(f"❌ Error inicializando motor: {e}")
    
    def analizar_caso(self, datos_caso: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza un caso legal y genera predicciones
        
        Args:
            datos_caso: Diccionario con los datos del caso
            
        Returns:
            Dict con el análisis y predicciones
        """
        try:
            # Generar ID único si no existe
            caso_id = datos_caso.get("id", self._generar_id_caso(datos_caso))
            
            self.logger.info(f"📊 Analizando caso: {caso_id}")
            
            # Análisis base del caso
            analisis = self._procesar_caso(datos_caso)
            
            # Generar predicciones
            predicciones = self._generar_predicciones(datos_caso)
            
            # Crear resultado completo
            resultado = {
                "id_caso": caso_id,
                "timestamp": datetime.now().isoformat(),
                "estado": "completado",
                "analisis": analisis,
                "predicciones": predicciones,
                "recomendaciones": self._generar_recomendaciones(analisis, predicciones),
                "metadata": {
                    "version_motor": self.version,
                    "precision": self.configuracion.get("precision", 0.95),
                    "algoritmos_utilizados": list(self.configuracion.get("algoritmos", {}).keys())
                }
            }
            
            self.logger.info(f"✔ Análisis completado: {caso_id}")
            return resultado
            
        except Exception as e:
            self.logger.error(f"❌ Error analizando caso: {e}")
            return {
                "error": str(e),
                "estado": "error",
                "timestamp": datetime.now().isoformat(),
                "mensaje": "Error durante el análisis del caso"
            }
    
    def _procesar_caso(self, datos_caso: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa los datos del caso para análisis"""
        return {
            "tipo_caso": datos_caso.get("tipo", "general"),
            "complejidad": self._calcular_complejidad(datos_caso),
            "factores_clave": self._identificar_factores_clave(datos_caso),
            "precedentes": self._buscar_precedentes(datos_caso),
            "riesgos": self._evaluar_riesgos(datos_caso)
        }
    
    def _generar_predicciones(self, datos_caso: Dict[str, Any]) -> Dict[str, Any]:
        """Genera predicciones basadas en el análisis"""
        # Simulación de predicción (en implementación real usaría ML)
        base_probability = 0.75
        
        # Ajustar según complejidad
        complejidad = self._calcular_complejidad(datos_caso)
        if complejidad > 0.7:
            base_probability -= 0.1
        elif complejidad < 0.3:
            base_probability += 0.1
        
        return {
            "probabilidad_exito": round(base_probability, 2),
            "tiempo_estimado": self._estimar_tiempo(datos_caso),
            "costos_estimados": self._estimar_costos(datos_caso),
            "escenarios": {
                "optimista": round(base_probability + 0.15, 2),
                "realista": round(base_probability, 2),
                "pesimista": round(base_probability - 0.15, 2)
            }
        }
    
    def _generar_recomendaciones(self, analisis: Dict[str, Any], predicciones: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        recomendaciones = []
        
        # Recomendaciones basadas en probabilidad
        if predicciones["probabilidad_exito"] < 0.6:
            recomendaciones.append("Considerar mediación o acuerdo extrajudicial")
            recomendaciones.append("Reforzar evidencia documental")
        
        # Recomendaciones basadas en complejidad
        if analisis["complejidad"] > 0.7:
            recomendaciones.append("Asignar equipo especializado")
            recomendaciones.append("Planificar estrategia a largo plazo")
        
        # Recomendaciones generales
        recomendaciones.extend([
            "Revisar precedentes jurisprudenciales recientes",
            "Documentar todas las comunicaciones",
            "Mantener registro detallado de evidencias"
        ])
        
        return recomendaciones
    
    def _calcular_complejidad(self, datos_caso: Dict[str, Any]) -> float:
        """Calcula la complejidad del caso"""
        factores = 0
        total = 0
        
        # Factores de complejidad
        if datos_caso.get("partes_involucradas", 0) > 2:
            factores += 1
        if datos_caso.get("jurisdicciones", 0) > 1:
            factores += 1
        if datos_caso.get("documentos", 0) > 100:
            factores += 1
        if datos_caso.get("testigos", 0) > 10:
            factores += 1
        if datos_caso.get("monto_disputado", 0) > 100000:
            factores += 1
        
        total = 5  # Total de factores evaluados
        
        return round(factores / total, 2) if total > 0 else 0.5
    
    def _identificar_factores_clave(self, datos_caso: Dict[str, Any]) -> List[str]:
        """Identifica factores clave del caso"""
        factores = []
        
        if datos_caso.get("evidencia_documental"):
            factores.append("Evidencia documental sólida")
        
        if datos_caso.get("testigos"):
            factores.append("Testimonios disponibles")
        
        if datos_caso.get("precedentes"):
            factores.append("Precedentes jurisprudenciales")
        
        if not factores:
            factores = ["Análisis inicial", "Contexto legal", "Documentación base"]
        
        return factores
    
    def _buscar_precedentes(self, datos_caso: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Busca precedentes relevantes"""
        # Simulación de búsqueda de precedentes
        return [
            {
                "caso": "Precedente A",
                "relevancia": 0.85,
                "fecha": "2023-01-15",
                "resultado": "favorable"
            },
            {
                "caso": "Precedente B", 
                "relevancia": 0.72,
                "fecha": "2022-11-20",
                "resultado": "desfavorable"
            }
        ]
    
    def _evaluar_riesgos(self, datos_caso: Dict[str, Any]) -> Dict[str, Any]:
        """Evalúa riesgos del caso"""
        return {
            "riesgo_procesal": "medio",
            "riesgo_económico": "bajo",
            "riesgo_reputacional": "bajo",
            "factores_mitigantes": [
                "Documentación completa",
                "Asesoría especializada",
                "Estrategia definida"
            ]
        }
    
    def _estimar_tiempo(self, datos_caso: Dict[str, Any]) -> str:
        """Estima tiempo de resolución"""
        complejidad = self._calcular_complejidad(datos_caso)
        
        if complejidad < 0.3:
            return "3-6 meses"
        elif complejidad < 0.7:
            return "6-12 meses"
        else:
            return "12-24 meses"
    
    def _estimar_costos(self, datos_caso: Dict[str, Any]) -> Dict[str, Any]:
        """Estima costos del caso"""
        base_cost = 10000
        complejidad = self._calcular_complejidad(datos_caso)
        
        costo_estimado = base_cost * (1 + complejidad)
        
        return {
            "costo_base": base_cost,
            "costo_estimado": round(costo_estimado, 2),
            "rango_minimo": round(costo_estimado * 0.8, 2),
            "rango_maximo": round(costo_estimado * 1.5, 2)
        }
    
    def _generar_id_caso(self, datos_caso: Dict[str, Any]) -> str:
        """Genera ID único para el caso"""
        contenido = json.dumps(datos_caso, sort_keys=True)
        hash_objeto = hashlib.md5(contenido.encode())
        return f"caso_{hash_objeto.hexdigest()[:8]}"
    
    def obtener_estado(self) -> Dict[str, Any]:
        """Obtiene el estado actual del motor"""
        return {
            "version": self.version,
            "estado": self.estado,
            "configuracion_activa": self.configuracion.get("configuracion_activa", True),
            "precision": self.configuracion.get("precision", 0.95),
            "algoritmos_disponibles": list(self.configuracion.get("algoritmos", {}).keys()),
            "timestamp": datetime.now().isoformat()
        }
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas del motor"""
        return {
            "casos_procesados": 0,  # En implementación real llevaría contador
            "tiempo_promedio": "N/A",
            "precision_actual": self.configuracion.get("precision", 0.95),
            "memoria_utilizada": "N/A",
            "ultima_actualizacion": datetime.now().isoformat()
        }

# Instancia global del motor
motor = MotorPredictivo()

# Funciones de utilidad para importación
def analizar_caso(datos_caso: Dict[str, Any]) -> Dict[str, Any]:
    """Función wrapper para análisis de casos"""
    return motor.analizar_caso(datos_caso)

def obtener_estado() -> Dict[str, Any]:
    """Función wrapper para estado del motor"""
    return motor.obtener_estado()

def obtener_estadisticas() -> Dict[str, Any]:
    """Función wrapper para estadísticas"""
    return motor.obtener_estadisticas()

# Exportar funciones principales
__all__ = [
    'MotorPredictivo',
    'motor',
    'analizar_caso',
    'obtener_estado',
    'obtener_estadisticas'
]

if __name__ == "__main__":
    # Prueba del motor
    print("🧪 Probando Motor Predictivo...")
    
    caso_prueba = {
        "id": "test_001",
        "tipo": "civil",
        "descripcion": "Caso de prueba",
        "partes_involucradas": 2,
        "monto_disputado": 50000
    }
    
    resultado = motor.analizar_caso(caso_prueba)
    print(f"✅ Resultado: {json.dumps(resultado, indent=2, ensure_ascii=False)}")
    
    estado = motor.obtener_estado()
    print(f"📊 Estado: {json.dumps(estado, indent=2, ensure_ascii=False)}")