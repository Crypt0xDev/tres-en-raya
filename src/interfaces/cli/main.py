# main.py

import os
import sys
from .game_logic import start_game

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    """Función principal para ejecutar el juego local"""
    print("¡Bienvenido al juego Tres en Raya!")
    print("Instrucciones: Usa los números del 1-9 para seleccionar una casilla:")
    print("1 | 2 | 3")
    print("---------")
    print("4 | 5 | 6")
    print("---------")
    print("7 | 8 | 9\n")

    while True:
        start_game()
        play_again = input("¿Quieres jugar otra vez? (s/n): ").lower()
        if play_again not in ["s", "si", "sí", "y", "yes"]:
            print("¡Gracias por jugar!")
            break


if __name__ == "__main__":
    main()
