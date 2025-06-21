import httpx
import time

BASE_URL = "https://gpt-legal-backend.onrender.com"

def quick_test():
    client = httpx.Client(timeout=15.0)
    tests = [
        ("GET", "/", None),
        ("POST", "/predict", {"texto": "contrato laboral informal"}),
        ("GET", "/legislacion/buscar", {"palabra": "contrato"}),
    ]
    
    print("⚡ QUICK TEST - Endpoints Críticos")
    print("=" * 40)
    
    passed = 0
    for method, endpoint, data in tests:
        try:
            if method == "GET" and isinstance(data, dict):
                r = client.get(f"{BASE_URL}{endpoint}", params=data)
            elif method == "POST":
                r = client.post(f"{BASE_URL}{endpoint}", json=data)
            else:
                r = client.get(f"{BASE_URL}{endpoint}")
            
            if r.status_code < 400:
                print(f"✅ {method} {endpoint}")
                passed += 1
            else:
                print(f"❌ {method} {endpoint} - {r.status_code}")
        except Exception as e:
            print(f"❌ {method} {endpoint} - Error")
    
    success_rate = (passed / len(tests)) * 100
    print(f"\n📊 Resultado: {passed}/{len(tests)} ({success_rate:.0f}%)")
    
    if success_rate == 100:
        print("🎉 TODO FUNCIONAL - Listo para deploy!")
    elif success_rate >= 66:
        print("✅ MAYORMENTE FUNCIONAL - Deploy OK")
    else:
        print("⚠️  PROBLEMAS DETECTADOS")
    
    client.close()
    return success_rate >= 66

if __name__ == "__main__":
    quick_test()
