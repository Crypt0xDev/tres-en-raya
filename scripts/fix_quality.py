#!/usr/bin/env python3
"""
Script para arreglar automáticamente problemas de calidad de código.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_fix_command(cmd, description):
    """Ejecuta un comando de arreglo automático."""
    print(f"\n🔧 {description}...")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        return False


def main():
    """Ejecuta arreglos automáticos de calidad."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("🎨 Arreglando problemas de calidad de código automáticamente...")
    
    # Comandos de arreglo automático
    fixes = [
        {
            "cmd": [sys.executable, "-m", "black", "src", "tests"],
            "description": "Formateo automático con Black"
        },
        {
            "cmd": [sys.executable, "-m", "isort", "src", "tests"],
            "description": "Ordenamiento de imports con isort"
        }
    ]
    
    success_count = 0
    
    for fix in fixes:
        if run_fix_command(fix["cmd"], fix["description"]):
            success_count += 1
    
    print(f"\n📊 Completados {success_count}/{len(fixes)} arreglos automáticos")
    
    if success_count == len(fixes):
        print("\n🎉 ¡Todos los arreglos automáticos completados!")
        print("💡 Ejecuta 'python scripts/quality_check.py' para verificar el estado")
    else:
        print("\n⚠️  Algunos arreglos no pudieron completarse automáticamente")
        print("🔍 Revisa los errores manualmente")


if __name__ == "__main__":
    main()