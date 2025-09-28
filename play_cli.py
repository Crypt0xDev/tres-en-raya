#!/usr/bin/env python3
"""
Script para ejecutar el Tres en Raya por línea de comandos
"""

import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Ejecutar el juego CLI"""
    print("🎮 TRES EN RAYA - LÍNEA DE COMANDOS")
    print("=" * 40)
    
    try:
        from src.interfaces.cli.game_logic import start_game
        
        print("¡Iniciando juego en modo CLI...")
        print("Instrucciones:")
        print("- Usa números del 1-9 para seleccionar casillas")
        print("- El tablero se numera así:")
        print("  1 | 2 | 3")
        print("  ---------") 
        print("  4 | 5 | 6")
        print("  ---------")
        print("  7 | 8 | 9")
        print("\n¡Empezando la partida!")
        print("-" * 40)
        
        # Iniciar el juego
        start_game()
        
    except KeyboardInterrupt:
        print("\n\n👋 ¡Gracias por jugar Tres en Raya!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Asegúrate de estar en el directorio correcto del proyecto.")

if __name__ == "__main__":
    main()