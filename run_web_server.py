#!/usr/bin/env python3
"""
Script principal para ejecutar el servidor web del juego Tres en Raya
"""
import sys
import os

# Agregar el directorio src al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Ahora importar y ejecutar la aplicación Flask
from interfaces.web.app import app

if __name__ == "__main__":
    print("🎮 Iniciando servidor web para Tres en Raya...")
    print("🌐 Servidor disponible en: http://localhost:5000")
    print("🎯 Ctrl+C para detener el servidor")
    print("-" * 50)
    
    # Configurar para desarrollo local
    app.run(debug=True, host='127.0.0.1', port=5000)