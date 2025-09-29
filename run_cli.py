#!/usr/bin/env python3
"""
Script para ejecutar el juego Tres en Raya en modo consola/CLI
"""
import sys
import os

# Agregar el directorio src al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Importar y ejecutar la versión CLI del juego
from interfaces.cli.main import main

if __name__ == "__main__":
    main()