"""
Test de integración para CI/CD GitHub Actions.

Este test valida que el proyecto funciona correctamente 
en el entorno de GitHub Actions.
"""

import unittest
import sys
import os
from pathlib import Path


class TestCIIntegration(unittest.TestCase):
    """Tests para validar integración con CI/CD."""
    
    def test_python_environment(self):
        """Verifica que el entorno Python está configurado correctamente."""
        self.assertGreaterEqual(sys.version_info.major, 3)
        self.assertGreaterEqual(sys.version_info.minor, 9)
        
    def test_project_structure_exists(self):
        """Verifica que la estructura del proyecto existe."""
        project_root = Path(__file__).parent.parent
        
        # Verificar carpetas principales
        self.assertTrue((project_root / 'game').exists())
        self.assertTrue((project_root / 'interfaces').exists())
        self.assertTrue((project_root / 'application').exists())
        self.assertTrue((project_root / 'persistence').exists())
        self.assertTrue((project_root / 'infrastructure').exists())
        
    def test_domain_imports_work(self):
        """Verifica que los imports del dominio funcionan."""
        try:
            from game.entities.board import Board, BoardSize
            from game.entities.player import Player, PlayerType
            from game.entities.game_session import GameSession
            # Si llegamos aquí, los imports funcionan
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f'Domain imports failed: {e}')
            
    def test_core_functionality(self):
        """Test básico de funcionalidad core."""
        from game.entities.board import Board, BoardSize
        from game.entities.player import Player, PlayerType, PlayerSymbol
        
        # Crear entidades básicas
        board = Board(BoardSize.STANDARD)
        player = Player("TestPlayer", PlayerType.HUMAN)
        player.assign_symbol(PlayerSymbol.X)
        
        # Verificar que funcionan
        self.assertEqual(board.size, 3)
        self.assertEqual(player.name, "TestPlayer")
        self.assertEqual(player.symbol, PlayerSymbol.X)
        
    def test_web_adapter_imports(self):
        """Verifica que el adaptador web se puede importar."""
        try:
            from interfaces.web_ui.flask_adapter import FlaskWebAdapter
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f'Web adapter import failed: {e}')


if __name__ == '__main__':
    # Configurar path para imports
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    unittest.main()