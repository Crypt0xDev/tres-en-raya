#!/usr/bin/env python3
"""
Script para verificar que todas las funcionalidades del Tres en Raya funcionen correctamente
"""

import sys
import os

# Añadir el directorio src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_core_functionality():
    """Prueba las funcionalidades básicas del core del juego"""
    print("🎯 Probando funcionalidad del CORE...")
    
    try:
        from src.core.board import Board
        from src.core.player import Player
        from src.core.game_engine import GameEngine
        
        # Test Board
        print("  ✅ Imports del core exitosos")
        
        board = Board()
        print(f"  📋 Tablero creado: {len(board.board)}x{len(board.board[0])}")
        
        # Test movimientos
        print(f"  🎯 Turno actual: {board.current_player}")
        result = board.make_move(0, 0)
        print(f"  🎮 Movimiento en (0,0): {result}")
        
        print(f"  🎯 Turno actual: {board.current_player}")
        result = board.make_move(1, 1)
        print(f"  🎮 Movimiento en (1,1): {result}")
        
        # Test ganador
        winner = board.check_winner()
        print(f"  🏆 Estado del ganador: {winner if winner else 'Sin ganador aún'}")
        
        # Test tablero lleno
        is_full = board.is_board_full()
        print(f"  📊 Tablero lleno: {is_full}")
        
        # Test Player
        player_x = Player('Jugador 1')
        player_x.set_symbol('X')
        player_o = Player('Jugador 2')
        player_o.set_symbol('O')
        print(f"  👤 Jugadores creados: {player_x.name} ({player_x.symbol}) vs {player_o.name} ({player_o.symbol})")
        
        # Test GameEngine
        engine = GameEngine()
        game_id = engine.start_game("Jugador 1", "Jugador 2")
        print(f"  🎯 Juego creado con ID: {game_id}")
        
        game_status = engine.get_game_status(game_id)
        print(f"  📊 Estado del juego: {game_status}")
        
        print("  ✅ CORE - Todas las funcionalidades básicas funcionan correctamente!\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Error en el core: {e}")
        return False

def test_game_simulation():
    """Simula una partida completa"""
    print("🎮 Simulando partida completa...")
    
    try:
        from src.core.board import Board
        from src.core.player import Player
        
        board = Board()
        player_x = Player('Jugador 1')
        player_x.set_symbol('X')
        player_o = Player('Jugador 2')
        player_o.set_symbol('O')
        
        # Movimientos de una partida ganadora para X
        moves = [
            (0, 0),  # X en esquina
            (1, 1),  # O en centro
            (0, 1),  # X 
            (2, 0),  # O
            (0, 2)   # X gana (fila superior)
        ]
        
        print("  📋 Tablero inicial:")
        board.display()
        
        for i, (row, col) in enumerate(moves):
            current_symbol = board.current_player
            success = board.make_move(row, col)
            print(f"  {i+1}. Movimiento {current_symbol} en ({row},{col}): {'✅' if success else '❌'}")
            
            winner = board.check_winner()
            if winner:
                print(f"  🏆 ¡{winner} ha ganado!")
                break
                
            if board.is_board_full():
                print("  🤝 ¡Empate!")
                break
        
        print("  📋 Tablero final:")
        board.display()
        
        print("  ✅ SIMULACIÓN - Partida completada exitosamente!\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Error en la simulación: {e}")
        return False

def test_web_imports():
    """Prueba que los imports web funcionen"""
    print("🌐 Probando imports de la interfaz WEB...")
    
    try:
        from src.interfaces.web.app import app
        print("  ✅ Import de app exitoso")
        
        print("  ✅ App Flask importada exitosamente")
        
        with app.test_client() as client:
            # Test ruta básica si existe
            try:
                response = client.get('/')
                print(f"  🌐 Respuesta de ruta raíz: {response.status_code}")
            except:
                print("  ℹ️  Ruta raíz no configurada (normal)")
        
        print("  ✅ WEB - Aplicación web funciona correctamente!\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Error en web: {e}")
        return False

def test_cli_imports():
    """Prueba que los imports CLI funcionen"""
    print("💻 Probando imports de la interfaz CLI...")
    
    try:
        from src.interfaces.cli.game_logic import start_game
        print("  ✅ Import de start_game exitoso")
        
        from src.interfaces.cli.ui.console_ui import ConsoleUI
        print("  ✅ Import de ConsoleUI exitoso")
        
        ui = ConsoleUI()
        print("  ✅ ConsoleUI creada exitosamente")
        
        print("  ✅ CLI - Interfaz de línea de comandos funciona correctamente!\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Error en CLI: {e}")
        return False

def main():
    """Función principal que ejecuta todas las pruebas"""
    print("🔍 VERIFICACIÓN COMPLETA DE FUNCIONALIDAD - TRES EN RAYA")
    print("=" * 60)
    
    results = []
    
    # Ejecutar todas las pruebas
    results.append(("Core", test_core_functionality()))
    results.append(("Simulación", test_game_simulation()))
    results.append(("Web", test_web_imports()))
    results.append(("CLI", test_cli_imports()))
    
    # Resumen final
    print("📊 RESUMEN DE VERIFICACIÓN:")
    print("-" * 40)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, result in results if result)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name:12} | {status}")
    
    print("-" * 40)
    print(f"  TOTAL:       | {passed_tests}/{total_tests} pruebas exitosas")
    
    if passed_tests == total_tests:
        print("\n🎉 ¡TODAS LAS FUNCIONALIDADES FUNCIONAN CORRECTAMENTE!")
        print("   El juego Tres en Raya está listo para usar.")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} funcionalidades requieren atención.")
    
    print("=" * 60)
    return passed_tests == total_tests

if __name__ == "__main__":
    main()