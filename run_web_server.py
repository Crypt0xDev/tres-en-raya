#!/usr/bin/env python3
"""
Tres en Raya - Ejecutor Web Completo con Screaming Architecture

Este script ejecuta la aplicación completa usando el FlaskWebAdapter
que implementa toda la arquitectura del dominio.
"""

import sys
import os
from pathlib import Path

# Configurar PYTHONPATH al directorio raíz del proyecto
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """
    Ejecuta la aplicación web completa de Tres en Raya.
    """
    print("🎮 Tres en Raya - Screaming Architecture Complete")
    print("=" * 60)
    print("🏗️ Arquitectura: Screaming Architecture")
    print("🎯 Dominio: Juego de Tres en Raya")
    print("🚚 Delivery: Adaptador Flask Web")
    print("💾 Persistencia: Repositorio en Memoria")
    print("🧪 Casos de Uso: StartNewGame, MakeMove")
    print("=" * 60)
    
    try:
        # Importar el adaptador web completo
        from delivery_mechanisms.web_ui.flask_adapter import FlaskWebAdapter
        
        print("🌐 Iniciando servidor web...")
        print("🏠 URL: http://127.0.0.1:5000")
        print("🎮 Interfaz principal: http://127.0.0.1:5000/")
        print("📄 GitHub Pages: http://127.0.0.1:5000/github-pages")
        print("🔌 API: http://127.0.0.1:5000/api/game/")
        print("🛑 Presiona Ctrl+C para detener")
        print("=" * 60)
        
        # Crear y ejecutar el adaptador web
        web_adapter = FlaskWebAdapter()
        web_adapter.run(
            debug=True,
            host='127.0.0.1',
            port=5000
        )
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Verifica que la estructura de Screaming Architecture esté completa")
        return 1
        
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())