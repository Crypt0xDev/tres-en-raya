#!/usr/bin/env python3
"""
Script para probar las APIs del Tres en Raya
"""

import requests
import json

def test_web_api():
    """Probar la API REST principal"""
    print("🌐 Probando API REST en http://127.0.0.1:5000")
    print("-" * 50)
    
    base_url = "http://127.0.0.1:5000/api"
    
    try:
        # Test 1: Iniciar juego
        print("1️⃣ Iniciando nuevo juego...")
        response = requests.post(f"{base_url}/start_game", 
                               json={"game_mode": "local", "first_player": "X"},
                               timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Respuesta: {response.json()}")
        else:
            print(f"   ⚠️  Respuesta: {response.text}")
        
        # Test 2: Obtener estado del juego
        print("\n2️⃣ Obteniendo estado del juego...")
        response = requests.get(f"{base_url}/get_game_state?game_id=test_123", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Respuesta: {response.json() if response.status_code == 200 else response.text}")
        
        # Test 3: Hacer movimiento
        print("\n3️⃣ Haciendo movimiento...")
        response = requests.post(f"{base_url}/make_move",
                               json={"row": 0, "col": 0, "game_id": "test_123"},
                               timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Respuesta: {response.json() if response.status_code == 200 else response.text}")
        
    except requests.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("💡 Asegúrate de que la aplicación web esté ejecutándose")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def test_multiplayer_server():
    """Probar el servidor multiplayer"""
    print("\n🎮 Probando servidor multiplayer en http://127.0.0.1:5001")
    print("-" * 55)
    
    try:
        response = requests.get("http://127.0.0.1:5001", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Servidor multiplayer respondiendo correctamente")
        else:
            print("⚠️  Servidor multiplayer con respuesta inesperada")
            
    except requests.ConnectionError:
        print("❌ Error: No se puede conectar al servidor multiplayer")
        print("💡 Asegúrate de que el servidor multiplayer esté ejecutándose")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def main():
    """Función principal"""
    print("🔍 PRUEBAS DE CONECTIVIDAD - TRES EN RAYA")
    print("=" * 55)
    
    test_web_api()
    test_multiplayer_server()
    
    print("\n" + "=" * 55)
    print("🎯 RESUMEN:")
    print("   • Aplicación Web: http://127.0.0.1:5000")
    print("   • Servidor Multiplayer: http://127.0.0.1:5001") 
    print("   • CLI: python play_cli.py")

if __name__ == "__main__":
    main()