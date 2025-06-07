#!/usr/bin/env python3
"""
Script de testing completo para Forensic Legal Cognition API 4.1
Prueba todos los endpoints con casos reales y manejo de errores
"""

import json
import time
import argparse
from typing import Optional, Dict, Any

try:
    import httpx
except ModuleNotFoundError:
    import pytest
    pytest.skip("httpx not installed", allow_module_level=True)

try:
    import ssl
except ModuleNotFoundError:
    import pytest
    pytest.skip("ssl module missing", allow_module_level=True)

# Configuración
BASE_URL = "https://gpt-legal-backend.onrender.com"
LOCAL_URL = "http://127.0.0.1:8000"
TIMEOUT = 30.0

class APITester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.client = httpx.Client(timeout=TIMEOUT)
        self.results = []

    def log_result(self, test_name: str, success: bool, response_data: Any = None, error: str = None):
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
        url = f"{self.base_url}{endpoint}"
        try:
            return self.client.request(method, url, **kwargs)
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return None

    def test_health_check(self):
        response = self.safe_request("GET", "/")
        if response and response.status_code == 200:
            data = response.json()
            self.log_result("Health Check", True, data)
            return data
        else:
            self.log_result("Health Check", False, error=f"Status: {response.status_code if response else 'No response'}")
            return None

    def test_status_json(self):
        response = self.safe_request("GET", "/status/json")
        if response and response.status_code == 200:
            data = response.json()
            self.log_result("Status JSON", True, data)
            return data
        else:
            self.log_result("Status JSON", False, error=f"Status: {response.status_code if response else 'No response'}")
            return None

    def test_error_handling(self):
        error_tests = [
            ("POST", "/predict", {"invalid": "data"}),
            ("POST", "/reflexion/", {"documento_analizado": ""}),
            ("GET", "/legislacion/buscar", {"palabra": "a"}),
            ("GET", "/legislacion/norma/999999999", None),
            ("POST", "/api/prediccion/", {"contexto": "muy corto"}),
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
            if response and response.status_code >= 400:
                try:
                    _ = response.json()
                    self.log_result(test_name, True, f"Error handled: {response.status_code}")
                    handled_errors += 1
                except:
                    self.log_result(test_name, True, f"Error handled: {response.status_code} (no JSON)")
                    handled_errors += 1
            else:
                self.log_result(test_name, False, error="Error not properly handled")

        return handled_errors >= len(error_tests) // 2

    def run_comprehensive_test(self):
        print("\U0001F680 Ejecutando tests comprehensivos de Forensic Legal Cognition API 4.1")
        print("=" * 70)
        start_time = time.time()

        health = self.test_health_check()
        status = self.test_status_json()
        error_handling = self.test_error_handling()

        # Test reales simulados
        real_tests = [
            ("POST", "/reflexion/", {"mensaje": "Analiza el principio de legalidad en el proceso penal chileno"}),
            ("POST", "/predict", {"hechos": "El imputado fue sorprendido sustrayendo especies desde el local comercial."}),
            ("POST", "/api/prediccion/", {"contexto": "Hechos ocurridos en un procedimiento administrativo de fiscalización."}),
            ("POST", "/vision/", {"imagen_base64": "data:image/png;base64,iVBORw0KG..."}),
            ("GET", "/legislacion/buscar", {"palabra": "responsabilidad civil"}),
            ("GET", "/api/bcn/norma/1234", None),
            ("GET", "/api/bcn/norma/5678", None),
            ("POST", "/forensics/search", {"consulta": "beneficiario final empresa offshore"}),
            ("POST", "/text-search", {"consulta": "principio de legalidad"}),
        ]

        for method, endpoint, data in real_tests:
            if method == "GET" and isinstance(data, dict):
                response = self.safe_request(method, endpoint, params=data)
            elif method == "GET":
                response = self.safe_request(method, endpoint)
            else:
                response = self.safe_request(method, endpoint, json=data)

            test_name = f"{method} {endpoint}"
            if response and response.status_code == 200:
                self.log_result(test_name, True, response.json())
            else:
                self.log_result(test_name, False, error=f"Status: {response.status_code if response else 'No response'}")

        total_time = time.time() - start_time
        passed = sum([bool(health), bool(status), error_handling])
        total = 3
        print("=" * 70)
        print(f"✅ Tests exitosos: {passed}/{total} ({(passed/total)*100:.1f}%)")
        print(f"⏱️  Tiempo total: {total_time:.2f} segundos")
        print("=" * 70)
        return passed == total

def main():
    parser = argparse.ArgumentParser(description="Test Forensic Legal Cognition API")
    parser.add_argument("--url", default=BASE_URL, help=f"URL base del API (default: {BASE_URL})")
    parser.add_argument("--local", action="store_true", help="Usar URL local")
    parser.add_argument("--quick", action="store_true", help="Tests rápidos solamente")
    parser.add_argument("--full", action="store_true", help="Tests completos")
    args = parser.parse_args()

    url = LOCAL_URL if args.local else args.url
    print(f"\U0001F31F Ejecutando test en: {url}")
    tester = APITester(url)

    if args.quick:
        tester.test_health_check()
        tester.test_status_json()
        tester.test_error_handling()
    else:
        tester.run_comprehensive_test()

if __name__ == "__main__":
    main()
