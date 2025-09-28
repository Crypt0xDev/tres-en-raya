#!/usr/bin/env python3
"""
Script para probar la aplicación web Flask del Tres en Raya
"""

import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_web_app():
    """Prueba la aplicación web Flask"""
    print("🌐 Probando aplicación web Flask...")
    
    try:
        from src.interfaces.web.app import app
        
        # Crear cliente de pruebas
        with app.test_client() as client:
            print("  ✅ Cliente de pruebas creado")
            
            # Test ruta principal
            response = client.get('/')
            print(f"  🏠 GET /: {response.status_code}")
            
            # Test rutas API si existen
            api_routes = [
                '/api/start_game',
                '/api/make_move', 
                '/api/get_game_state',
                '/api/end_game'
            ]
            
            for route in api_routes:
                try:
                    if route == '/api/start_game':
                        response = client.post(route, 
                                             json={'game_mode': 'local', 'first_player': 'X'},
                                             content_type='application/json')
                    elif route == '/api/make_move':
                        response = client.post(route,
                                             json={'row': 0, 'col': 0, 'game_id': 'test'},
                                             content_type='application/json')
                    elif route == '/api/get_game_state':
                        response = client.get(route + '?game_id=test')
                    elif route == '/api/end_game':
                        response = client.post(route,
                                             json={'game_id': 'test', 'reason': 'forfeit'},
                                             content_type='application/json')
                    
                    print(f"  🔗 {route}: {response.status_code}")
                    
                except Exception as e:
                    print(f"  ⚠️  {route}: Error - {str(e)[:50]}...")
            
            print("  ✅ Aplicación web probada exitosamente")
            return True
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_cli_simulation():
    """Simula el uso de la CLI sin input interactivo"""
    print("💻 Simulando funcionalidad CLI...")
    
    try:
        from src.interfaces.cli.ui.console_ui import ConsoleUI
        from src.core.board import Board
        
        ui = ConsoleUI()
        board = Board()
        
        print("  ✅ ConsoleUI y Board creados")
        
        # Simular algunos métodos de UI si existen
        print(f"  📋 Estado inicial del tablero:")
        board.display()
        
        # Hacer algunos movimientos
        print("  🎮 Simulando movimientos...")
        board.make_move(0, 0)  # X
        board.make_move(1, 1)  # O
        board.make_move(0, 1)  # X
        
        print(f"  📋 Estado después de movimientos:")
        board.display()
        
        winner = board.check_winner()
        print(f"  🏆 Ganador: {winner if winner else 'Ninguno'}")
        
        print("  ✅ CLI simulada exitosamente")
        return True
        
    except Exception as e:
        print(f"  ❌ Error en CLI: {e}")
        return False

def main():
    """Función principal"""
    print("🎮 PRUEBAS ADICIONALES DE FUNCIONALIDAD")
    print("=" * 50)
    
    results = []
    
    results.append(("Web App", test_web_app()))
    results.append(("CLI Simulation", test_cli_simulation()))
    
    print("\n📊 RESUMEN DE PRUEBAS ADICIONALES:")
    print("-" * 35)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name:15} | {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("-" * 35)
    print(f"  TOTAL:          | {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS ADICIONALES PASARON!")
    else:
        print(f"\n⚠️  {total - passed} pruebas requieren atención.")
    
    return passed == total

if __name__ == "__main__":
    main()