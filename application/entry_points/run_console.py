"""
Punto de Entrada para la Aplicación CLI del Tres en Raya.

Este es el punto de entrada principal que orquesta la aplicación CLI,
conectando todos los componentes siguiendo Screaming Architecture.
"""

import sys
import os
from pathlib import Path

# Añadir el directorio raíz al path para importaciones
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from interfaces.console_ui.cli_adapter import CLIAdapter


def create_cli_app():
    """
    Factory para crear la aplicación CLI.
    
    Returns:
        Instancia configurada de CLIAdapter
    """
    return CLIAdapter()


def main():
    """
    Función principal para ejecutar la aplicación CLI.
    
    Esta función:
    - Crea la aplicación CLI usando el factory
    - Configura el entorno de consola
    - Inicia la interfaz de línea de comandos
    """
    print("🎮 Tres en Raya - Screaming Architecture")
    print("=" * 50)
    print("🏗️ Arquitectura: Screaming Architecture 100%")
    print("💻 Interfaz: CLI (Consola)")
    print("💾 Persistencia: En memoria")
    print("🎯 Dominio: Juego de Tres en Raya")
    print("=" * 50)
    
    try:
        # Crear aplicación CLI
        cli_app = create_cli_app()
        
        # Ejecutar aplicación
        cli_app.run()
        
    except KeyboardInterrupt:
        print("\\n🛑 Aplicación interrumpida por el usuario")
    except Exception as e:
        print(f"❌ Error al ejecutar la aplicación CLI: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()