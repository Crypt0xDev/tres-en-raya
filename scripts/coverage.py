#!/usr/bin/env python3
"""
Script para ejecutar tests con cobertura de código y generar reportes.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_coverage():
    """Ejecuta tests con medición de cobertura."""
    print("🧪 Ejecutando tests con cobertura...")
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Ejecutar pytest con cobertura
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "--cov=src",
        "--cov-report=html:htmlcov",
        "--cov-report=term-missing", 
        "--cov-report=xml:coverage.xml",
        "--cov-branch",
        "-v"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ Tests completados exitosamente!")
        
        # Mostrar ubicación de reportes
        print("\n📊 Reportes de cobertura generados:")
        print(f"  - HTML: {project_root}/htmlcov/index.html")
        print(f"  - XML:  {project_root}/coverage.xml")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error ejecutando tests: {e}")
        return False


def open_coverage_report():
    """Abre el reporte HTML de cobertura."""
    import webbrowser
    
    html_report = Path("htmlcov/index.html")
    if html_report.exists():
        webbrowser.open(f"file://{html_report.absolute()}")
        print("🌐 Abriendo reporte de cobertura en el navegador...")
    else:
        print("❌ No se encontró el reporte HTML. Ejecuta los tests primero.")


def main():
    """Función principal del script."""
    if len(sys.argv) > 1 and sys.argv[1] == "--open":
        open_coverage_report()
    else:
        success = run_coverage()
        if success:
            print("\n💡 Tip: Usa 'python scripts/coverage.py --open' para ver el reporte HTML")


if __name__ == "__main__":
    main()