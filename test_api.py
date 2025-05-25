#!/usr/bin/env python3
"""
Script de testing completo para Forensic Legal Cognition API 4.1
Prueba todos los endpoints con casos reales y manejo de errores
"""

import httpx
import json
import time
from typing import Optional, Dict, Any

# Configuración
BASE_URL = "https://gpt-legal-backend.onrender.com"
LOCAL_URL = "http://localhost:8000"
TIMEOUT = 30.0

class APITester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.client = httpx.Client(timeout=TIMEOUT)
        self.results = []
        
    def log_result(self, test_name: str, success: bool, response_data: Any = None, error: str = None):
        """Registra resultado de test"""
        result = {
            "test": test_name,
            "success": success,
            "timestamp": time.strftime("%H:%M:%S"),
            "response_preview": str(response_data)[:200] if response_data else None,
            "error": error
        }
        self.results.append(result)
        
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
        if error:
            print(f"   Error: {error}")
        if response_data and success:
            print(f"   Response: {str(response_data)[:100]}...")
        print()

    def safe_request(self, method: str, endpoint: str, **kwargs) -> Optional[httpx.Response]:
        """Realiza request seguro con manejo de errores"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.client.request(method, url, **kwargs)
            return response
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return None

    def test_health_check(self):
        """Test 1: Health Check"""
        response = self.safe_request("GET", "/")
        if response and response.status_code == 200:
            data = response.json()
            self.log_result("Health Check", True, data)
            return data
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            self.log_result("Health Check", False, error=error_msg)
            return None

    def test_status_json(self):
        """Test 2: Status JSON"""
        response = self.safe_request("GET", "/status/json")
        if response and response.status_code == 200:
            data = response.json()
            self.log_result("Status JSON", True, data)
            return data
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            self.log_result("Status JSON", False, error=error_msg)
            return None

    def test_predict_endpoint(self):
        """Test 3: Predict Endpoint"""
        test_cases = [
            {"texto": "Trabajador sin contrato formal recibe pagos irregulares desde hace 6 meses"},
            {"input": "Empresa despide trabajador sindicalizado sin seguir protocolo legal"},
            {"contexto": "Contrato de arriendo con cláusulas abusivas y aumento arbitrario de renta"}
        ]
        
        success_count = 0
        for i, payload in enumerate(test_cases):
            response = self.safe_request("POST", "/predict", json=payload)
            test_name = f"Predict Case {i+1}"
            
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    self.log_result(test_name, True, data)
                    success_count += 1
                except:
                    self.log_result(test_name, False, error="Invalid JSON response")
            else:
                error_msg = f"Status: {response.status_code if response else 'No response'}"
                self.log_result(test_name, False, error=error_msg)
        
        return success_count == len(test_cases)

    def test_reflexion_endpoint(self):
        """Test 4: Reflexión Jurídica"""
        payload = {
            "documento_analizado": "Decreto que establece procedimiento administrativo sin garantizar el derecho a ser oído ni la debida fundamentación de los actos administrativos",
            "criterios": ["constitucionalidad", "convencionalidad", "contradicción normativa", "due process"]
        }
        
        response = self.safe_request("POST", "/reflexion/", json=payload)
        if response and response.status_code == 200:
            try:
                data = response.json()
                # Verificar estructura de respuesta dual
                if "json" in data and "markdown" in data:
                    self.log_result("Reflexión Jurídica", True, data)
                    return True
                else:
                    self.log_result("Reflexión Jurídica", False, error="Missing dual response structure")
                    return False
            except:
                self.log_result("Reflexión Jurídica", False, error="Invalid JSON response")
                return False
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            self.log_result("Reflexión Jurídica", False, error=error_msg)
            return False

    def test_prediccion_bayesiana(self):
        """Test 5: Predicción Bayesiana"""
        payload = {
            "contexto": "Empresa constructora ejecuta obra pública sin cumplir especificaciones técnicas del contrato, generando riesgo estructural y sobrecostos al Estado. El director de obra omite informar las irregularidades detectadas."
        }
        
        response = self.safe_request("POST", "/api/prediccion/", json=payload)
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.log_result("Predicción Bayesiana", True, data)
                return True
            except:
                self.log_result("Predicción Bayesiana", False, error="Invalid JSON response")
                return False
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            self.log_result("Predicción Bayesiana", False, error=error_msg)
            return False

    def test_vision_forense(self):
        """Test 6: Análisis de Visión Forense"""
        payload = {
            "image_id": "evidencia_contrato_adulterado_2025_caso_001.pdf"
        }
        
        response = self.safe_request("POST", "/vision/", json=payload)
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.log_result("Análisis de Visión", True, data)
                return True
            except:
                self.log_result("Análisis de Visión", False, error="Invalid JSON response")
                return False
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            self.log_result("Análisis de Visión", False, error=error_msg)
            return False

    def test_buscar_norma(self):
        """Test 7: Buscar Norma en BCN"""
        test_queries = ["contrato", "responsabilidad civil", "procedimiento administrativo"]
        
        successful_searches = 0
        found_ids = []
        
        for query in test_queries:
            response = self.safe_request("GET", "/legislacion/buscar", params={"palabra": query})
            test_name = f"Buscar '{query}'"
            
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    self.log_result(test_name, True, data)
                    successful_searches += 1
                    
                    # Extraer ID si está disponible
                    if "id" in data and data["id"]:
                        found_ids.append(data["id"])
                except:
                    self.log_result(test_name, False, error="Invalid JSON response")
            else:
                error_msg = f"Status: {response.status_code if response else 'No response'}"
                self.log_result(test_name, False, error=error_msg)
        
        return successful_searches > 0, found_ids

    def test_obtener_norma(self, id_norma: int):
        """Test 8: Obtener Norma por ID"""
        response = self.safe_request("GET", f"/legislacion/norma/{id_norma}")
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.log_result(f"Obtener Norma {id_norma}", True, data)
                return True
            except:
                self.log_result(f"Obtener Norma {id_norma}", False, error="Invalid JSON response")
                return False
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            self.log_result(f"Obtener Norma {id_norma}", False, error=error_msg)
            return False

    def test_bcn_parser(self, id_norma: int):
        """Test 9: BCN Parser Directo"""
        response = self.safe_request("GET", f"/api/bcn/norma/{id_norma}")
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.log_result(f"BCN Parser {id_norma}", True, data)
                return True
            except:
                self.log_result(f"BCN Parser {id_norma}", False, error="Invalid JSON response")
                return False
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            self.log_result(f"BCN Parser {id_norma}", False, error=error_msg)
            return False

    def test_forensics_search(self):
        """Test 10: Búsqueda Forense"""
        test_queries = [
            "beneficiario final empresa offshore",
            "transparencia activa municipios",
            "declaración patrimonio autoridades",
            "conflicto intereses funcionarios públicos"
        ]
        
        successful_searches = 0
        for query in test_queries:
            response = self.safe_request("GET", "/forensics/search", params={"pregunta": query})
            test_name = f"Forensics '{query[:30]}...'"
            
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    self.log_result(test_name, True, data)
                    successful_searches += 1
                except:
                    self.log_result(test_name, False, error="Invalid JSON response")
            else:
                error_msg = f"Status: {response.status_code if response else 'No response'}"
                self.log_result(test_name, False, error=error_msg)
        
        return successful_searches > 0

    def test_text_search(self):
        """Test 11: Búsqueda Textual"""
        test_queries = ["responsabilidad civil", "debido proceso", "principio legalidad"]
        
        successful_searches = 0
        for query in test_queries:
            response = self.safe_request("GET", "/text-search", params={"palabra": query})
            test_name = f"Text Search '{query}'"
            
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    self.log_result(test_name, True, data)
                    successful_searches += 1
                except:
                    self.log_result(test_name, False, error="Invalid JSON response")
            else:
                error_msg = f"Status: {response.status_code if response else 'No response'}"
                self.log_result(test_name, False, error=error_msg)
        
        return successful_searches > 0

    def test_error_handling(self):
        """Test 12: Manejo de Errores"""
        error_tests = [
            ("POST", "/predict", {"invalid": "data"}),
            ("POST", "/reflexion/", {"documento_analizado": ""}),
            ("GET", "/legislacion/buscar", {"palabra": "a"}),  # Muy corto
            ("GET", "/legislacion/norma/999999999"),  # ID inexistente
            ("POST", "/api/prediccion/", {"contexto": "muy corto"}),  # Contexto insuficiente
        ]
        
        handled_errors = 0
        for method, endpoint, data in error_tests:
            if method == "GET" and isinstance(data, dict):
                response = self.safe_request(method, endpoint, params=data)
            elif method == "GET":
                response = self.safe_request(method, endpoint)
            else:
                response = self.safe_request(method, endpoint, json=data)
            
            test_name = f"Error Handling {method} {endpoint}"
            
            # Verificar que el error se maneja apropiadamente (4xx o 5xx)
            if response and response.status_code >= 400:
                try:
                    error_data = response.json()
                    self.log_result(test_name, True, f"Error handled: {response.status_code}")
                    handled_errors += 1
                except:
                    self.log_result(test_name, True, f"Error handled: {response.status_code} (no JSON)")
                    handled_errors += 1
            else:
                self.log_result(test_name, False, error="Error not properly handled")
        
        return handled_errors >= len(error_tests) // 2  # Al menos 50% de errores manejados

    def run_comprehensive_test(self):
        """Ejecuta todos los tests"""
        print("🚀 Iniciando tests comprehensivos de Forensic Legal Cognition API 4.1")
        print("=" * 70)
        
        start_time = time.time()
        
        # Tests básicos
        health_data = self.test_health_check()
        status_data = self.test_status_json()
        
        # Tests de predicción
        predict_success = self.test_predict_endpoint()
        reflexion_success = self.test_reflexion_endpoint()
        prediccion_success = self.test_prediccion_bayesiana()
        
        # Tests de análisis
        vision_success = self.test_vision_forense()
        
        # Tests de legislación
        search_success, found_ids = self.test_buscar_norma()
        
        # Usar IDs encontrados o defaults para tests de normas
        test_ids = found_ids[:2] if found_ids else [1234, 5678]
        norma_results = []
        bcn_results = []
        
        for test_id in test_ids:
            norma_results.append(self.test_obtener_norma(test_id))
            bcn_results.append(self.test_bcn_parser(test_id))
        
        # Tests de búsqueda especializada
        forensics_success = self.test_forensics_search()
        text_search_success = self.test_text_search()
        
        # Tests de manejo de errores
        error_handling_success = self.test_error_handling()
        
        # Calcular estadísticas
        total_time = time.time() - start_time
        successful_tests = sum([
            bool(health_data), bool(status_data), predict_success, reflexion_success,
            prediccion_success, vision_success, search_success, any(norma_results),
            any(bcn_results), forensics_success, text_search_success, error_handling_success
        ])
        total_tests = 12
        success_rate = (successful_tests / total_tests) * 100
        
        # Reporte final
        print("=" * 70)
        print("📊 REPORTE FINAL DE TESTS")
        print("=" * 70)
        print(f"⏱️  Tiempo total: {total_time:.2f} segundos")
        print(f"✅ Tests exitosos: {successful_tests}/{total_tests} ({success_rate:.1f}%)")
        print(f"🌐 URL testeada: {self.base_url}")
        
        # Estado por categorías
        categories = {
            "Sistema": [bool(health_data), bool(status_data)],
            "Predicción": [predict_success, reflexion_success, prediccion_success],
            "Análisis": [vision_success],
            "Legislación": [search_success, any(norma_results), any(bcn_results)],
            "Búsqueda": [forensics_success, text_search_success],
            "Errores": [error_handling_success]
        }
        
        print("\n📋 Estado por categorías:")
        for category, results in categories.items():
            cat_success = sum(results)
            cat_total = len(results)
            cat_rate = (cat_success / cat_total) * 100 if cat_total > 0 else 0
            status = "🟢" if cat_rate >= 80 else "🟡" if cat_rate >= 50 else "🔴"
            print(f"   {status} {category}: {cat_success}/{cat_total} ({cat_rate:.0f}%)")
        
        # Recomendaciones
        print("\n💡 Recomendaciones:")
        if success_rate >= 90:
            print("   🎉 API funcionando excelentemente!")
        elif success_rate >= 70:
            print("   ✅ API en buen estado, revisar tests fallidos")
        elif success_rate >= 50:
            print("   ⚠️  API funcional pero requiere atención")
        else:
            print("   🚨 API requiere revisión urgente")
        
        if not search_success:
            print("   📚 Verificar conectividad con BCN")
        if not any(norma_results):
            print("   🔍 Revisar endpoints de legislación")
        if not error_handling_success:
            print("   🛡️  Mejorar manejo de errores")
        
        self.client.close()
        return success_rate >= 70

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Forensic Legal Cognition API")
    parser.add_argument("--url", default=BASE_URL, help=f"URL base del API (default: {BASE_URL})")
    parser.add_argument("--local", action="store_true", help="Usar URL local")
    parser.add_argument("--quick", action="store_true", help="Tests rápidos solamente")
    
    args = parser.parse_args()
    
    if args.local:
        test_url = LOCAL_URL
    else:
        test_url = args.url
    
    print(f"🎯 Testing API en: {test_url}")
    
    tester = APITester(test_url)
    
    if args.quick:
        # Tests rápidos
        tester.test_health_check()
        tester.test_status_json()
        tester.test_predict_endpoint()
    else:
        # Tests completos
        success = tester.run_comprehensive_test()
        exit(0 if success else 1)

if __name__ == "__main__":
    main()