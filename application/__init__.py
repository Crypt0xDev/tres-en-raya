"""
Application Layer - Capa de aplicación.

Este módulo exporta los componentes de la capa de aplicación
que orquestan los casos de uso para la aplicación web con IA, 
torneos y funcionalidad online.
"""

from .entry_points import (
    TicTacToeWebApp,
    create_app,
    web_main
)

__all__ = [
    # Web Application - Única interfaz del sistema  
    'TicTacToeWebApp',
    'create_app',
    'web_main',
]
