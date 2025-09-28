#!/usr/bin/env python3
"""
Script para ejecutar herramientas de calidad de código.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(cmd, description):
    """Ejecuta un comando y muestra el resultado."""
    print(f"\n🔍 {description}...")
    print(f"Ejecutando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado exitosamente")
        if result.stdout:
            print("Output:", result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}")
        print("Error:", e.stderr[:500] + "..." if len(e.stderr) > 500 else e.stderr)
        return False


def main():
    """Ejecuta todas las herramientas de calidad."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("🎨 Ejecutando herramientas de calidad de código...")
    
    # Lista de herramientas y comandos
    tools = [
        {
            "cmd": [sys.executable, "-m", "black", "--check", "src", "tests"],
            "description": "Verificación de formato con Black",
            "fix_cmd": [sys.executable, "-m", "black", "src", "tests"]
        },
        {
            "cmd": [sys.executable, "-m", "isort", "--check-only", "src", "tests"],
            "description": "Verificación de imports con isort",
            "fix_cmd": [sys.executable, "-m", "isort", "src", "tests"]
        },
        {
            "cmd": [sys.executable, "-m", "flake8", "src", "tests"],
            "description": "Linting con flake8"
        },
        {
            "cmd": [sys.executable, "-m", "mypy", "src"],
            "description": "Verificación de tipos con mypy"
        },
        {
            "cmd": [sys.executable, "-m", "bandit", "-r", "src", "-f", "json"],
            "description": "Análisis de seguridad con bandit"
        }
    ]
    
    results = []
    
    # Verificar si las herramientas están disponibles
    print("🔧 Verificando disponibilidad de herramientas...")
    
    for tool in tools:
        success = run_command(tool["cmd"], tool["description"])
        results.append({
            "name": tool["description"],
            "success": success,
            "fix_cmd": tool.get("fix_cmd")
        })
    
    # Mostrar resumen
    print("\n📊 RESUMEN DE CALIDAD:")
    print("=" * 50)
    
    all_passed = True
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"{status} - {result['name']}")
        if not result["success"]:
            all_passed = False
    
    if all_passed:
        print("\n🎉 ¡Todas las verificaciones de calidad pasaron!")
        return 0
    else:
        print("\n🔧 Para arreglar automáticamente algunos problemas, ejecuta:")
        print("python scripts/fix_quality.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())