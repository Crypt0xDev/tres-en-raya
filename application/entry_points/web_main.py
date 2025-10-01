"""
Web Entry Point - Punto de entrada para la aplicación web.

Este módulo implementa el punto de entrada principal para ejecutar
el juego Tres en Raya como aplicación web usando Flask.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al PYTHONPATH
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
sys.path.insert(0, str(project_root))

# Importar después de configurar el PYTHONPATH
try:
    from interfaces.web_ui.flask_adapter import FlaskWebAdapter
except ImportError as e:
    print(f"Error al importar FlaskWebAdapter: {e}")
    sys.exit(1)


class TicTacToeWebApp:
    """
    TicTacToeWebApp - Aplicación web para Tres en Raya.
    
    Wrapper simplificado alrededor del FlaskWebAdapter siguiendo
    los principios de Screaming Architecture.
    """
    
    def __init__(self):
        """
        Inicializa la aplicación web de Tres en Raya.
        """
        # Usar directamente el adaptador web que ya funciona
        try:
            self.web_adapter = FlaskWebAdapter()
            self.app = self.web_adapter.app
        except Exception as e:
            print(f"Error inicializando FlaskWebAdapter: {e}")
            raise
    
    def run(self, host='127.0.0.1', port=5000, debug=True):
        """
        Ejecuta la aplicación web.
        
        Args:
            host: Dirección del servidor
            port: Puerto del servidor
            debug: Modo debug
        """
        print(f"🌐 Iniciando Tres en Raya Web Server")
        print(f"🏠 Servidor: http://{host}:{port}")
        print(f"🔧 Modo: {'Debug' if debug else 'Producción'}")
        print("=" * 60)
        
        try:
            self.app.run(host=host, port=port, debug=debug, threaded=True)
        except KeyboardInterrupt:
            print("\n👋 Servidor detenido por el usuario")
        except Exception as e:
            print(f"\n❌ Error al iniciar el servidor: {e}")
            sys.exit(1)
    
    def get_flask_app(self):
        """
        Obtiene la instancia de Flask configurada.
        
        Returns:
            Instancia de Flask
        """
        return self.app


def create_app():
    """
    Factory function para crear la aplicación Flask.
    
    Returns:
        Instancia de Flask configurada
    """
    web_app = TicTacToeWebApp()
    return web_app.get_flask_app()


def main():
    """
    Función principal para ejecutar la aplicación web.
    
    Returns:
        Código de salida
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Servidor web para el juego Tres en Raya'
    )
    
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host del servidor (default: 127.0.0.1)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Puerto del servidor (default: 5000)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Ejecutar en modo debug'
    )
    
    parser.add_argument(
        '--no-debug',
        action='store_true',
        help='Ejecutar en modo producción'
    )
    
    args = parser.parse_args()
    
    # Determinar modo debug
    debug = True
    if args.no_debug:
        debug = False
    elif args.debug:
        debug = True
    
    # Crear y ejecutar aplicación
    try:
        web_app = TicTacToeWebApp()
        web_app.run(host=args.host, port=args.port, debug=debug)
        return 0
    except Exception as e:
        print(f"Error fatal: {e}")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)