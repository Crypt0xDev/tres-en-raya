#!/usr/bin/env python3
"""
🛠️ Tres en Raya - Herramienta de Desarrollo - Screaming Architecture

Script de desarrollo para el juego Tres en Raya que facilita
tareas comunes de desarrollo siguiendo los principios de 
Screaming Architecture.

Esta herramienta permite realizar tareas de desarrollo manteniendo
el enfoque en el dominio del juego como protagonista.
"""

import sys
import os
import subprocess
import argparse
import json
from pathlib import Path

# Agregar el directorio raíz al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def show_architecture():
    """Mostrar la estructura de Screaming Architecture."""
    print("🏗️ TRES EN RAYA - SCREAMING ARCHITECTURE 100%")
    print("=" * 60)
    print("🎯 DOMINIO: Juego de Tres en Raya")
    print("🎮 La arquitectura 'GRITA' sobre el juego, no sobre la tecnología")
    print("=" * 60)
    print()
    
    architecture_tree = """
📁 tres-en-raya/
├── 🎮 game/                     # DOMINIO DEL JUEGO
│   ├── entities/               # Entidades del negocio
│   │   ├── board.py           # Tablero del juego
│   │   ├── player.py          # Jugador del juego
│   │   └── game_session.py    # Sesión de partida
│   ├── use_cases/             # Casos de uso del juego
│   │   ├── start_new_game.py  # Iniciar nueva partida
│   │   ├── make_move.py       # Realizar movimiento
│   │   └── check_winner.py    # Verificar ganador
│   ├── services/              # Servicios del dominio
│   │   ├── ai_opponent.py     # Oponente AI
│   │   └── score_calculator.py # Calculadora de puntuación
│   └── rules/                 # Reglas del juego
│       ├── game_rules.py      # Reglas principales
│       └── victory_conditions.py # Condiciones de victoria
│
├── 🚀 application/             # ORQUESTACIÓN
│   └── entry_points/          # Puntos de entrada
│       ├── cli_app.py         # Aplicación CLI
│       ├── web_app.py         # Aplicación Web
│       └── multiplayer_server.py # Servidor multiplayer
│
├── 🔌 delivery_mechanisms/     # INTERFACES EXTERNAS
│   ├── web/                   # Interfaz web
│   │   └── flask_adapter.py   # Adaptador Flask
│   └── console/               # Interfaz consola
│       └── cli_adapter.py     # Adaptador CLI
│
├── 💾 persistence/             # PERSISTENCIA
│   ├── repositories/          # Repositorios
│   └── storage/              # Almacenamiento
│
├── ⚙️ infrastructure/          # INFRAESTRUCTURA
│   ├── configuration/         # Configuración
│   └── external_services/     # Servicios externos
│
└── 🧪 tests/                   # TESTS ARQUITECTÓNICOS
    ├── unit/game/             # Tests del dominio
    ├── integration/           # Tests de integración
    └── e2e/                  # Tests end-to-end
    """
    
    print(architecture_tree)
    print("=" * 60)
    print("💡 PRINCIPIOS APLICADOS:")
    print("   ✅ La estructura GRITA 'Tres en Raya'")
    print("   ✅ El dominio es independiente de tecnologías")
    print("   ✅ Los casos de uso son explícitos y visibles")
    print("   ✅ Las interfaces son adaptadores")
    print("   ✅ La persistencia es un detalle")
    print("=" * 60)

def check_dependencies():
    """Verificar dependencias del proyecto."""
    print("📦 Verificando Dependencias")
    print("=" * 40)
    
    # Leer requirements desde su nueva ubicación
    requirements_files = [
        "infrastructure/development/requirements.txt",
        "infrastructure/development/requirements-dev.txt", 
        "infrastructure/development/requirements-prod.txt",
        "infrastructure/development/requirements-ci.txt"
    ]
    
    for req_file in requirements_files:
        if os.path.exists(req_file):
            print(f"\n📋 {req_file}:")
            with open(req_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            import importlib
                            package_name = line.split('==')[0].split('>=')[0].split('<=')[0]
                            importlib.import_module(package_name.replace('-', '_'))
                            print(f"   ✅ {line}")
                        except ImportError:
                            print(f"   ❌ {line} (no instalado)")

def run_linting():
    """Ejecutar linting del código."""
    print("🔍 Ejecutando Análisis de Código")
    print("=" * 40)
    
    # Linting commands
    commands = [
        # Flake8 para estilo de código
        "flake8 game/ application/ delivery_mechanisms/ persistence/ infrastructure/ --max-line-length=100 --ignore=E501,W503",
        
        # Black para formateo automático (dry-run)
        "black --check --diff game/ application/ delivery_mechanisms/ persistence/ infrastructure/",
        
        # Mypy para type checking
        "mypy game/ application/ --ignore-missing-imports"
    ]
    
    for cmd in commands:
        print(f"\n🔍 Ejecutando: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Análisis exitoso")
            else:
                print("⚠️  Se encontraron issues:")
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(result.stderr)
        except Exception as e:
            print(f"❌ Error: {e}")

def generate_documentation():
    """Generar documentación del proyecto."""
    print("📚 Generando Documentación")
    print("=" * 40)
    
    # Crear estructura de documentación
    docs_structure = {
        "SCREAMING_ARCHITECTURE.md": """# Screaming Architecture - Tres en Raya

## ¿Qué es Screaming Architecture?

La Screaming Architecture es un principio donde la estructura del proyecto 
'grita' sobre qué hace la aplicación, no sobre qué frameworks utiliza.

## Aplicación en Tres en Raya

Nuestro proyecto está estructurado para que sea inmediatamente obvio 
que se trata de un juego de Tres en Raya:

- `game/` - Todo lo relacionado con el JUEGO
- `game/entities/` - Las entidades del JUEGO (Board, Player, GameSession)
- `game/use_cases/` - Los casos de uso del JUEGO (StartNewGame, MakeMove)
- `game/services/` - Los servicios del JUEGO (AIOpponent, ScoreCalculator)

La tecnología (Flask, CLI, etc.) está relegada a adaptadores.
""",
        
        "DOMAIN_MODEL.md": """# Modelo del Dominio - Tres en Raya

## Entidades Principales

### Board (Tablero)
- Representa el tablero de 3x3 del juego
- Maneja la lógica de colocación de movimientos
- Detecta condiciones de victoria y empate

### Player (Jugador)  
- Representa un jugador humano o AI
- Mantiene estadísticas y configuración
- Puede ser X u O

### GameSession (Sesión de Juego)
- Coordina una partida completa
- Mantiene el estado del juego
- Gestiona turnos de jugadores

## Casos de Uso

### StartNewGame
- Inicia una nueva partida
- Configura jugadores y tablero
- Establece estado inicial

### MakeMove
- Procesa un movimiento del jugador
- Valida el movimiento según reglas
- Actualiza estado del juego

### CheckWinner
- Verifica condiciones de victoria
- Detecta empates
- Determina el resultado final
""",
        
        "API_DOCUMENTATION.md": """# API del Juego Tres en Raya

## Endpoints Web

### POST /api/games
Crear nueva partida
```json
{
  "player1_name": "Juan",
  "player2_name": "María", 
  "player2_type": "human"
}
```

### POST /api/moves
Realizar movimiento
```json
{
  "session_id": "abc123",
  "position": {"row": 1, "col": 1}
}
```

### GET /api/games/{session_id}
Obtener estado del juego
```json
{
  "session_id": "abc123",
  "board": [["X", "", ""], ["", "O", ""], ["", "", ""]],
  "current_player": "X",
  "status": "in_progress"
}
```

## CLI Commands

- `run_cli.py` - Iniciar juego en consola
- `run_web_server.py` - Iniciar servidor web
- `run_multiplayer.py` - Iniciar servidor multiplayer
- `run_tests.py` - Ejecutar tests
"""
    }
    
    # Crear archivos de documentación
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    for filename, content in docs_structure.items():
        doc_path = docs_dir / filename
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📄 Generado: {doc_path}")

def clean_project():
    """Limpiar archivos temporales del proyecto."""
    print("🧹 Limpiando Proyecto")
    print("=" * 30)
    
    # Patrones de archivos a limpiar
    clean_patterns = [
        "**/__pycache__",
        "**/*.pyc", 
        "**/*.pyo",
        ".pytest_cache",
        "htmlcov",
        ".coverage",
        "*.egg-info",
        ".mypy_cache"
    ]
    
    import glob
    
    for pattern in clean_patterns:
        files = glob.glob(pattern, recursive=True)
        for file_path in files:
            try:
                if os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
                    print(f"🗂️  Eliminado directorio: {file_path}")
                else:
                    os.remove(file_path)
                    print(f"🗃️  Eliminado archivo: {file_path}")
            except Exception as e:
                print(f"❌ Error eliminando {file_path}: {e}")

def main():
    """Función principal de la herramienta de desarrollo."""
    parser = argparse.ArgumentParser(
        description="🛠️ Herramienta de Desarrollo - Tres en Raya Screaming Architecture",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Comandos disponibles:
  python dev.py --architecture    # Mostrar estructura de Screaming Architecture
  python dev.py --deps          # Verificar dependencias
  python dev.py --lint          # Análisis de código
  python dev.py --docs          # Generar documentación
  python dev.py --clean         # Limpiar archivos temporales
  python dev.py --all           # Ejecutar todas las tareas
        """
    )
    
    parser.add_argument('--architecture', action='store_true', help='Mostrar estructura arquitectónica')
    parser.add_argument('--deps', action='store_true', help='Verificar dependencias')
    parser.add_argument('--lint', action='store_true', help='Ejecutar linting')
    parser.add_argument('--docs', action='store_true', help='Generar documentación')
    parser.add_argument('--clean', action='store_true', help='Limpiar proyecto')
    parser.add_argument('--all', action='store_true', help='Ejecutar todas las tareas')
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        # Si no se especifica nada, mostrar la arquitectura
        args.architecture = True
    
    try:
        if args.architecture or args.all:
            show_architecture()
            if args.all:
                print("\n")
                
        if args.deps or args.all:
            check_dependencies()
            if args.all:
                print("\n")
                
        if args.lint or args.all:
            run_linting()
            if args.all:
                print("\n")
                
        if args.docs or args.all:
            generate_documentation()
            if args.all:
                print("\n")
                
        if args.clean or args.all:
            clean_project()
            
    except KeyboardInterrupt:
        print("\n🛑 Operación interrumpida por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()