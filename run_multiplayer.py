#!/usr/bin/env python3
"""
Script para ejecutar el servidor multiplayer de Tres en Raya
"""

import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Ejecutar el servidor multiplayer"""
    print("🌐 TRES EN RAYA - SERVIDOR MULTIPLAYER")
    print("=" * 45)
    
    try:
        from src.multiplayer.server import app
        
        print("🚀 Iniciando servidor multiplayer...")
        print("📡 El servidor estará disponible en:")
        print("   - Local: http://127.0.0.1:5001")
        print("   - Red: http://0.0.0.0:5001")
        print("\n💡 Para conectarse desde otro dispositivo:")
        print("   - Usa la IP de esta máquina en puerto 5001")
        print("\n🎮 Funcionalidades del servidor:")
        print("   - Múltiples salas de juego simultáneas")
        print("   - Comunicación en tiempo real con WebSockets")
        print("   - Gestión automática de turnos")
        print("\n🔄 Presiona Ctrl+C para detener el servidor")
        print("-" * 45)
        
        # Configurar y ejecutar el servidor
        app.run(
            debug=True, 
            host='0.0.0.0', 
            port=5001,
            use_reloader=False  # Evitar problemas con socketio
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor multiplayer detenido")
        print("👋 ¡Gracias por usar el servidor!")
    except Exception as e:
        print(f"\n❌ Error al iniciar servidor: {e}")
        print("💡 Asegúrate de que el puerto 5001 esté disponible")

if __name__ == "__main__":
    main()