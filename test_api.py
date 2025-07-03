#!/usr/bin/env python3
"""
Script para probar los endpoints de la API.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Prueba el endpoint de salud."""
    print("=== Probando endpoint de salud ===")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_health_check_endpoint():
    """Prueba el endpoint de verificación de salud."""
    print("\n=== Probando endpoint de verificación de salud ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_default_config_endpoint():
    """Prueba el endpoint de configuración por defecto."""
    print("\n=== Probando endpoint de configuración por defecto ===")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/algoritmo-genetico/configuracion-defecto")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_validate_data_endpoint():
    """Prueba el endpoint de validación de datos."""
    print("\n=== Probando endpoint de validación de datos ===")
    
    # Datos de prueba
    test_data = {
        "debilidades": {
            "lectura": 0.4,
            "escritura": 0.6,
            "memoria": 0.5
        },
        "reactivos": [
            {
                "id_reactivo": 1,
                "lectura": 0.2,
                "escritura": 0.3,
                "memoria": 0.5
            },
            {
                "id_reactivo": 2,
                "lectura": 0.3,
                "escritura": 0.4,
                "memoria": 0.3
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/algoritmo-genetico/validar-datos",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_genetic_algorithm_endpoint():
    """Prueba el endpoint principal del algoritmo genético."""
    print("\n=== Probando endpoint del algoritmo genético ===")
    
    # Datos de prueba (los mismos del JSON de ejemplo)
    test_data = {
        "debilidades": {
            "lectura": 0.4,
            "escritura": 0.6,
            "memoria": 0.5
        },
        "reactivos": [
            {
                "id_reactivo": 1,
                "lectura": 0.2,
                "escritura": 0.3,
                "memoria": 0.5
            },
            {
                "id_reactivo": 2,
                "lectura": 0.3,
                "escritura": 0.4,
                "memoria": 0.3
            },
            {
                "id_reactivo": 3,
                "lectura": 0.2,
                "escritura": 0.3,
                "memoria": 0.5
            },
            {
                "id_reactivo": 4,
                "lectura": 0.5,
                "escritura": 0.7,
                "memoria": 0.4
            },
            {
                "id_reactivo": 5,
                "lectura": 0.4,
                "escritura": 0.5,
                "memoria": 0.6
            }
        ]
    }
    
    try:
        print("Enviando datos al algoritmo genético...")
        response = requests.post(
            f"{BASE_URL}/api/v1/algoritmo-genetico/ejecutar",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Resultado del algoritmo genético:")
            print(f"  Mejor individuo: {result['mejor_individuo']}")
            print(f"  Aptitud: {result['aptitud']}")
            print(f"  Generaciones: {result['generaciones']}")
            print(f"  Tamaño población final: {len(result['poblacion_final'])}")
        else:
            print(f"Error Response: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Ejecuta todas las pruebas."""
    print("🧪 Iniciando pruebas de la API del Algoritmo Genético\n")
    
    tests = [
        ("Endpoint de salud", test_health_endpoint),
        ("Endpoint de verificación de salud", test_health_check_endpoint),
        ("Endpoint de configuración por defecto", test_default_config_endpoint),
        ("Endpoint de validación de datos", test_validate_data_endpoint),
        ("Endpoint del algoritmo genético", test_genetic_algorithm_endpoint),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
            print(f"{'✅' if success else '❌'} {test_name}: {'PASÓ' if success else 'FALLÓ'}")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    print(f"\n=== Resumen de Pruebas ===")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"Pruebas pasadas: {passed}/{total}")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

