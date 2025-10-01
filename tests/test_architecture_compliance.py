"""
Análisis de conformidad con Screaming Architecture.

Este script verifica que el proyecto sigue correctamente los principios
de Screaming Architecture.
"""

import sys
from pathlib import Path

# Add project root to path for Screaming Architecture imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def check_screaming_architecture_compliance():
    """Verifica el cumplimiento de Screaming Architecture."""
    
    compliance_score = 0
    total_checks = 0
    issues = []
    
    print("🏗️ Análisis de Conformidad con Screaming Architecture")
    print("=" * 60)
    
    # 1. Verificar estructura de directorios
    print("\n1️⃣ ESTRUCTURA DE DIRECTORIOS:")
    required_dirs = {
        'game': 'Dominio central del juego',
        'application': 'Coordinadores de casos de uso',
        'interfaces': 'Adaptadores de interfaz',
        'persistence': 'Gestión de datos',
        'infrastructure': 'Configuración y herramientas'
    }
    
    for dir_name, description in required_dirs.items():
        dir_path = project_root / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print(f"   ✅ {dir_name}/ - {description}")
            compliance_score += 1
        else:
            print(f"   ❌ {dir_name}/ - Faltante")
            issues.append(f"Directorio {dir_name} no encontrado")
        total_checks += 1
    
    # 2. Verificar dominio como centro (game/)
    print("\n2️⃣ DOMINIO COMO CENTRO (game/):")
    domain_dirs = {
        'entities': 'Entidades del dominio',
        'use_cases': 'Casos de uso del negocio',
        'rules': 'Reglas del juego',
        'services': 'Servicios del dominio'
    }
    
    game_dir = project_root / 'game'
    for subdir, description in domain_dirs.items():
        subdir_path = game_dir / subdir
        if subdir_path.exists():
            print(f"   ✅ game/{subdir}/ - {description}")
            compliance_score += 1
        else:
            print(f"   ❌ game/{subdir}/ - Faltante")
            issues.append(f"Subdirectorio game/{subdir} no encontrado")
        total_checks += 1
    
    # 3. Verificar adaptadores (interfaces/)
    print("\n3️⃣ ADAPTADORES DE INTERFAZ:")
    adapter_dirs = {
        'web_ui': 'Adaptador web (Flask)',
        'console_ui': 'Adaptador CLI'
    }
    
    delivery_dir = project_root / 'interfaces'
    for adapter, description in adapter_dirs.items():
        adapter_path = delivery_dir / adapter
        if adapter_path.exists():
            print(f"   ✅ interfaces/{adapter}/ - {description}")
            compliance_score += 1
        else:
            print(f"   ❌ interfaces/{adapter}/ - Faltante")
            issues.append(f"Adaptador {adapter} no encontrado")
        total_checks += 1
    
    # 4. Verificar entry points
    print("\n4️⃣ PUNTOS DE ENTRADA:")
    entry_points = {
        'cli_main.py': 'Entrada CLI',
        'web_main.py': 'Entrada Web',
        'multiplayer_main.py': 'Entrada Multiplayer'
    }
    
    app_entry_dir = project_root / 'application' / 'entry_points'
    for entry_file, description in entry_points.items():
        entry_path = app_entry_dir / entry_file
        if entry_path.exists():
            print(f"   ✅ {entry_file} - {description}")
            compliance_score += 1
        else:
            print(f"   ❌ {entry_file} - Faltante")
            issues.append(f"Entry point {entry_file} no encontrado")
        total_checks += 1
    
    # 5. Verificar imports correctos
    print("\n5️⃣ IMPORTS Y DEPENDENCIAS:")
    try:
        # Verificar entidades del dominio
        from game.entities.board import Board, CellState, Position
        from game.entities.player import Player, PlayerType
        from game.entities.game_session import GameSession
        print("   ✅ Entidades del dominio importables")
        compliance_score += 1
        
        # Verificar adaptadores
        from interfaces.web_ui.flask_adapter import FlaskWebAdapter
        print("   ✅ Adaptador web importable")
        compliance_score += 1
        
        from interfaces.console_ui.cli_adapter import CLIAdapter
        print("   ✅ Adaptador CLI importable")
        compliance_score += 1
        
        # Verificar entry points
        from application.entry_points.web_main import TicTacToeWebApp
        print("   ✅ Entry point web importable")
        compliance_score += 1
        
        from application.entry_points.cli_main import TicTacToeCLIApp
        print("   ✅ Entry point CLI importable")
        compliance_score += 1
        
        from application.entry_points.multiplayer_main import TicTacToeMultiplayerApp
        print("   ✅ Entry point multiplayer importable")
        compliance_score += 1
        
        total_checks += 6
        
    except ImportError as e:
        print(f"   ❌ Error de importación: {e}")
        issues.append(f"Import error: {e}")
        total_checks += 6
    
    # 6. Verificar funcionalidad básica
    print("\n6️⃣ FUNCIONALIDAD BÁSICA:")
    try:
        # Test de creación de board
        board = Board()
        position = Position(0, 0)
        print("   ✅ Board y Position funcionales")
        compliance_score += 1
        
        # Test de player
        player = Player(name="Test", player_type=PlayerType.HUMAN)
        print("   ✅ Player funcional")
        compliance_score += 1
        
        # Test de web adapter
        web_adapter = FlaskWebAdapter()
        print("   ✅ Web adapter funcional")
        compliance_score += 1
        
        total_checks += 3
        
    except Exception as e:
        print(f"   ❌ Error de funcionalidad: {e}")
        issues.append(f"Functionality error: {e}")
        total_checks += 3
    
    # Calcular porcentaje de cumplimiento
    compliance_percentage = (compliance_score / total_checks) * 100 if total_checks > 0 else 0
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE CONFORMIDAD")
    print("=" * 60)
    print(f"✅ Checks pasados: {compliance_score}/{total_checks}")
    print(f"📈 Porcentaje de cumplimiento: {compliance_percentage:.1f}%")
    
    if compliance_percentage >= 95:
        print("🎉 EXCELENTE: Arquitectura totalmente conforme")
    elif compliance_percentage >= 80:
        print("👍 BUENO: Arquitectura mayormente conforme")
    elif compliance_percentage >= 60:
        print("⚠️ REGULAR: Necesita mejoras")
    else:
        print("❌ MALO: Requiere reestructuración")
    
    if issues:
        print("\n🔧 PROBLEMAS ENCONTRADOS:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    
    print("=" * 60)
    
    return compliance_percentage >= 80


if __name__ == "__main__":
    success = check_screaming_architecture_compliance()
    sys.exit(0 if success else 1)