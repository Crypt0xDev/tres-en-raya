"""
Tests de Validación de Screaming Architecture.

Este módulo contiene tests específicos para verificar que la implementación
sigue correctamente los principios de Screaming Architecture.
"""

import unittest
import sys
import os
from pathlib import Path
import importlib
import inspect


class TestScreamingArchitectureCompliance(unittest.TestCase):
    """Tests para validar cumplimiento de Screaming Architecture."""
    
    def setUp(self):
        """Configuración para tests."""
        self.project_root = Path(__file__).parent.parent
        if str(self.project_root) not in sys.path:
            sys.path.insert(0, str(self.project_root))
    
    def test_domain_independence_from_frameworks(self):
        """Verifica que el dominio no depende de frameworks externos."""
        forbidden_imports = [
            'flask', 'django', 'fastapi', 'bottle', 'tornado',
            'sqlalchemy', 'pymongo', 'redis', 'celery',
            'requests', 'urllib', 'http.client'
        ]
        
        domain_files = list(Path(self.project_root / 'game').rglob('*.py'))
        
        for file_path in domain_files:
            if '__pycache__' in str(file_path):
                continue
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for forbidden in forbidden_imports:
                self.assertNotIn(f'import {forbidden}', content, 
                    f'Domain file {file_path} imports forbidden framework: {forbidden}')
                self.assertNotIn(f'from {forbidden}', content,
                    f'Domain file {file_path} imports forbidden framework: {forbidden}')
    
    def test_domain_only_imports_standard_library_and_self(self):
        """Verifica que el dominio solo importa librería estándar y sí mismo."""
        domain_files = list(Path(self.project_root / 'game').rglob('*.py'))
        allowed_prefixes = ['typing', 'dataclasses', 'enum', 'datetime', 'uuid', 'random', 'game.', '.']
        
        for file_path in domain_files:
            if '__pycache__' in str(file_path):
                continue
                
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if line.startswith('from ') or line.startswith('import '):
                    # Extraer el módulo importado
                    if line.startswith('from '):
                        import_part = line.split(' ')[1]
                        module = import_part.split('.')[0] if not import_part.startswith('.') else '.'
                    else:  # import
                        module = line.split(' ')[1].split('.')[0]
                    
                    # Verificar que es permitido
                    is_allowed = any(module.startswith(prefix.rstrip('.')) for prefix in allowed_prefixes)
                    if not is_allowed:
                        print(f'Non-allowed import: {line} in {file_path}:{line_num}')
                    self.assertTrue(is_allowed, 
                        f'File {file_path}:{line_num} imports non-allowed module: {module}')
    
    def test_external_layers_depend_on_domain(self):
        """Verifica que las capas externas dependen del dominio."""
        from delivery_mechanisms.web_ui.flask_adapter import FlaskWebAdapter
        from application.entry_points.web_main import TicTacToeWebApp
        
        # Verificar que Flask adapter importa del dominio
        flask_file = Path(self.project_root / 'delivery_mechanisms/web_ui/flask_adapter.py')
        with open(flask_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn('from game.use_cases', content, 
            'Flask adapter should import game use cases')
        self.assertIn('from game.entities', content,
            'Flask adapter should import game entities')
    
    def test_use_cases_are_orchestrators(self):
        """Verifica que los use cases son orquestadores puros."""
        from game.use_cases.start_new_game import StartNewGameUseCase
        from game.use_cases.make_move import MakeMoveUseCase
        
        # Los use cases deben tener un método execute
        self.assertTrue(hasattr(StartNewGameUseCase, 'execute'))
        self.assertTrue(hasattr(MakeMoveUseCase, 'execute'))
        
        # Los use cases no deben extender de clases de framework
        self.assertEqual(StartNewGameUseCase.__bases__, (object,))
        self.assertEqual(MakeMoveUseCase.__bases__, (object,))
    
    def test_entities_contain_business_logic(self):
        """Verifica que las entidades contienen lógica de negocio."""
        from game.entities.board import Board
        from game.entities.player import Player
        from game.entities.game_session import GameSession
        
        # Board debe tener métodos de lógica de negocio
        board_methods = [method for method in dir(Board) if not method.startswith('_')]
        self.assertIn('place_move', board_methods)
        self.assertIn('get_winner', board_methods)
        self.assertIn('is_full', board_methods)
        
        # Player debe encapsular lógica del jugador
        player_methods = [method for method in dir(Player) if not method.startswith('_')]
        self.assertIn('assign_symbol', player_methods)
        
    def test_screaming_architecture_structure_clarity(self):
        """Verifica que la estructura 'grita' el propósito del dominio."""
        # La carpeta game debe existir y ser prominente
        game_dir = Path(self.project_root / 'game')
        self.assertTrue(game_dir.exists(), 'game/ directory should exist as domain center')
        
        # Subcarpetas del dominio deben reflejar conceptos del juego
        expected_subfolders = ['entities', 'rules', 'services', 'use_cases']
        for subfolder in expected_subfolders:
            self.assertTrue((game_dir / subfolder).exists(), 
                f'Domain should have {subfolder}/ subdirectory')
        
        # Archivos deben tener nombres que expresen conceptos del juego
        entity_files = list((game_dir / 'entities').glob('*.py'))
        entity_names = [f.stem for f in entity_files if f.stem != '__init__']
        game_concepts = ['board', 'player', 'game_session']
        
        for concept in game_concepts:
            self.assertIn(concept, entity_names,
                f'Entity {concept} should exist to express game domain')
    
    def test_no_circular_dependencies(self):
        """Verifica que no hay dependencias circulares."""
        # Este test básico verifica que se pueden importar todos los módulos del dominio
        try:
            from game.entities import Board, Player, GameSession
            from game.use_cases.start_new_game import StartNewGameUseCase
            from game.use_cases.make_move import MakeMoveUseCase
            from game.services.ai_opponent import AIOpponent
        except ImportError as e:
            self.fail(f'Circular dependency detected: {e}')
    
    def test_technology_agnostic_interfaces(self):
        """Verifica que las interfaces del dominio son agnósticas a tecnología.""" 
        from game.use_cases.start_new_game import StartNewGameRequest, StartNewGameResponse
        from game.use_cases.make_move import MakeMoveRequest, MakeMoveResponse
        
        # Los DTOs no deben contener tipos específicos de framework
        request_fields = StartNewGameRequest.__dataclass_fields__
        for field_name, field in request_fields.items():
            self.assertNotIn('flask', str(field.type).lower())
            self.assertNotIn('django', str(field.type).lower())


if __name__ == '__main__':
    unittest.main()