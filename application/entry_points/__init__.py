"""
Entry Points - Puntos de entrada de la aplicación.

Este módulo exporta el punto de entrada principal del sistema
para la aplicación web con IA, torneos y funcionalidad online.
"""

from .web_main import TicTacToeWebApp, create_app, main as web_main

__all__ = [
    # Web Application - Única interfaz del sistema
    'TicTacToeWebApp',
    'create_app', 
    'web_main',
]