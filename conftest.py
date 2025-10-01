"""
Configuración pytest para Screaming Architecture.
Asegura que todos los módulos del dominio sean encontrados correctamente.
"""
import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))