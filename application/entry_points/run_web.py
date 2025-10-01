"""
Punto de Entrada para la Aplicación Web del Tres en Raya.

Este es el punto de entrada principal que orquesta la aplicación web,
conectando todos los componentes siguiendo Screaming Architecture.
"""

import sys
import os
from pathlib import Path

# Añadir el directorio raíz al path para importaciones
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from delivery_mechanisms.web_ui.flask_adapter import FlaskWebAdapter


def create_app():
    """
    Factory para crear la aplicación web.
    
    Returns:
        Instancia configurada de FlaskWebAdapter
    """
    return FlaskWebAdapter()


def main():
    """
    Función principal para ejecutar la aplicación web.
    
    Esta función:
    - Crea la aplicación usando el factory
    - Configura el entorno
    - Inicia el servidor web
    """
    print("🎮 Iniciando Tres en Raya - Screaming Architecture")
    print("=" * 60)
    print("🏗️ Arquitectura: Screaming Architecture 100%")
    print("🌐 Interfaz: Web (Flask)")
    print("💾 Persistencia: En memoria") 
    print("🎯 Dominio: Juego de Tres en Raya")
    print("=" * 60)
    
    # Crear aplicación
    web_adapter = create_app()
    
    # Configuración del servidor
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print(f"🌐 Servidor iniciando en: http://{host}:{port}")
    print(f"🔧 Modo debug: {debug}")
    print(f"🎮 Interfaz principal: http://{host}:{port}/")
    print(f"📱 GitHub Pages: http://{host}:{port}/github-pages")
    print(f"🔄 API REST: http://{host}:{port}/api/")
    print("🛑 Presiona Ctrl+C para detener el servidor")
    print("=" * 60)
    
    try:
        # Ejecutar aplicación
        web_adapter.run(debug=debug, host=host, port=port)
    except KeyboardInterrupt:
        print("\\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()