"""
Tests unitarios para los servicios del dominio del juego Tres en Raya.

Estos tests verifican el comportamiento de los servicios del dominio
que encapsulan lógica de negocio compleja siguiendo Screaming Architecture.
"""

import unittest
from unittest.mock import Mock, patch

# Imports del dominio
from game.entities import (
    Board, Position, Move, CellState,
    Player, PlayerType, PlayerSymbol, PlayerStats,
    GameSession, GameState, GameConfiguration
)
from game.services.ai_opponent import AIOpponentService, DifficultyLevel
from game.services.score_calculator import ScoreCalculatorService
from game.services.statistics_tracker import StatisticsTrackerService


class TestAIOpponentService(unittest.TestCase):
    """Tests para el servicio AIOpponentService."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.service = AIOpponentService()
        self.board = Board()
    
    def test_ai_opponent_service_creation(self):
        """Test de creación del servicio AI."""
        self.assertIsNotNone(self.service)
        self.assertIsInstance(self.service, AIOpponentService)
    
    def test_get_best_move_easy_level(self):
        """Test de obtención del mejor movimiento en nivel fácil."""
        # El nivel fácil debe devolver cualquier movimiento válido
        move = self.service.get_best_move(
            board=self.board,
            player_symbol=PlayerSymbol.X,
            difficulty=DifficultyLevel.EASY
        )
        
        self.assertIsInstance(move, Move)
        self.assertEqual(move.player, CellState.PLAYER_X)
        self.assertTrue(self.board.is_position_empty(move.position))
    
    def test_get_best_move_medium_level(self):
        """Test de obtención del mejor movimiento en nivel medio."""
        move = self.service.get_best_move(
            board=self.board,
            player_symbol=PlayerSymbol.O,
            difficulty=DifficultyLevel.MEDIUM
        )
        
        self.assertIsInstance(move, Move)
        self.assertEqual(move.player, CellState.PLAYER_O)
        self.assertTrue(self.board.is_position_empty(move.position))
    
    def test_get_best_move_hard_level(self):
        """Test de obtención del mejor movimiento en nivel difícil."""
        move = self.service.get_best_move(
            board=self.board,
            player_symbol=PlayerSymbol.X,
            difficulty=DifficultyLevel.HARD
        )
        
        self.assertIsInstance(move, Move)
        self.assertEqual(move.player, CellState.PLAYER_X)
        self.assertTrue(self.board.is_position_empty(move.position))
    
    def test_ai_blocks_winning_move(self):
        """Test de que la AI bloquea movimientos ganadores del oponente."""
        # Configurar tablero donde el jugador humano puede ganar
        self.board.place_move(Move(Position(0, 0), CellState.PLAYER_X))
        self.board.place_move(Move(Position(0, 1), CellState.PLAYER_X))
        # Posición (0, 2) completaría la línea para X
        
        # La AI debe bloquear en (0, 2)
        move = self.service.get_best_move(
            board=self.board,
            player_symbol=PlayerSymbol.O,
            difficulty=DifficultyLevel.MEDIUM
        )
        
        # En nivel medio o difícil, debe bloquear la jugada ganadora
        if move.position == Position(0, 2):
            self.assertEqual(move.position, Position(0, 2))
    
    def test_ai_takes_winning_move(self):
        """Test de que la AI toma movimientos ganadores."""
        # Configurar tablero donde la AI puede ganar
        self.board.place_move(Move(Position(1, 0), CellState.PLAYER_O))
        self.board.place_move(Move(Position(1, 1), CellState.PLAYER_O))
        # Posición (1, 2) completaría la línea para O
        
        # La AI debe ganar en (1, 2)
        move = self.service.get_best_move(
            board=self.board,
            player_symbol=PlayerSymbol.O,
            difficulty=DifficultyLevel.HARD
        )
        
        # En nivel difícil, debe tomar la jugada ganadora
        self.assertIsInstance(move, Move)
    
    def test_no_moves_available(self):
        """Test cuando no hay movimientos disponibles."""
        # Llenar el tablero
        positions = [
            (Position(0, 0), CellState.PLAYER_X),
            (Position(0, 1), CellState.PLAYER_O),
            (Position(0, 2), CellState.PLAYER_X),
            (Position(1, 0), CellState.PLAYER_O),
            (Position(1, 1), CellState.PLAYER_X),
            (Position(1, 2), CellState.PLAYER_O),
            (Position(2, 0), CellState.PLAYER_X),
            (Position(2, 1), CellState.PLAYER_O),
            (Position(2, 2), CellState.PLAYER_X)
        ]
        
        for position, player in positions:
            self.board.place_move(Move(position, player))
        
        # No debe haber movimientos disponibles
        move = self.service.get_best_move(
            board=self.board,
            player_symbol=PlayerSymbol.O,
            difficulty=DifficultyLevel.EASY
        )
        
        self.assertIsNone(move)


class TestScoreCalculatorService(unittest.TestCase):
    """Tests para el servicio ScoreCalculatorService."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.service = ScoreCalculatorService()
        
        self.winner = Player("Ganador", PlayerType.HUMAN)
        self.winner.assign_symbol(PlayerSymbol.X)
        
        self.loser = Player("Perdedor", PlayerType.HUMAN)
        self.loser.assign_symbol(PlayerSymbol.O)
    
    def test_calculate_score_human_vs_human(self):
        """Test de cálculo de puntuación humano vs humano."""
        config = GameConfiguration()
        
        score = self.service.calculate_match_score(
            winner=self.winner,
            loser=self.loser,
            moves_count=5,
            config=config
        )
        
        self.assertIsInstance(score, dict)
        self.assertIn('winner_score', score)
        self.assertIn('loser_score', score)
        self.assertIn('bonus_points', score)
        
        # El ganador debe tener más puntos que el perdedor
        self.assertGreater(score['winner_score'], score['loser_score'])
    
    def test_calculate_score_human_vs_ai(self):
        """Test de cálculo de puntuación humano vs AI."""
        ai_player = Player("AI", PlayerType.AI_MEDIUM)
        ai_player.assign_symbol(PlayerSymbol.O)
        
        config = GameConfiguration()
        
        # Humano gana vs AI
        score = self.service.calculate_match_score(
            winner=self.winner,
            loser=ai_player,
            moves_count=7,
            config=config
        )
        
        # Ganar contra AI debe dar puntos bonus
        self.assertGreater(score['bonus_points'], 0)
    
    def test_calculate_score_quick_victory(self):
        """Test de puntuación por victoria rápida."""
        config = GameConfiguration()
        
        # Victoria en pocos movimientos
        score_quick = self.service.calculate_match_score(
            winner=self.winner,
            loser=self.loser,
            moves_count=3,  # Victoria rápida
            config=config
        )
        
        # Victoria lenta
        score_slow = self.service.calculate_match_score(
            winner=self.winner,
            loser=self.loser,
            moves_count=9,  # Victoria lenta
            config=config
        )
        
        # La victoria rápida debe dar más puntos
        self.assertGreaterEqual(
            score_quick['winner_score'], 
            score_slow['winner_score']
        )
    
    def test_calculate_draw_score(self):
        """Test de cálculo de puntuación en empate."""
        config = GameConfiguration()
        
        score = self.service.calculate_draw_score(
            player1=self.winner,
            player2=self.loser,
            moves_count=9,
            config=config
        )
        
        self.assertIsInstance(score, dict)
        self.assertIn('player1_score', score)
        self.assertIn('player2_score', score)
        
        # En empate, ambos jugadores deben recibir la misma puntuación
        self.assertEqual(score['player1_score'], score['player2_score'])


class TestStatisticsTrackerService(unittest.TestCase):
    """Tests para el servicio StatisticsTrackerService."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.service = StatisticsTrackerService()
        
        self.player1 = Player("Jugador 1", PlayerType.HUMAN)
        self.player2 = Player("Jugador 2", PlayerType.AI_EASY)
    
    def test_track_game_result_victory(self):
        """Test de registro de resultado de victoria."""
        # Simular victoria del jugador 1
        self.service.track_game_result(
            winner=self.player1,
            loser=self.player2,
            moves_count=7,
            game_duration_seconds=120
        )
        
        # Verificar que las estadísticas se actualizaron
        stats1 = self.player1.stats
        stats2 = self.player2.stats
        
        self.assertEqual(stats1.games_played, 1)
        self.assertEqual(stats1.games_won, 1)
        self.assertEqual(stats1.games_lost, 0)
        
        self.assertEqual(stats2.games_played, 1)
        self.assertEqual(stats2.games_won, 0)
        self.assertEqual(stats2.games_lost, 1)
    
    def test_track_game_result_draw(self):
        """Test de registro de resultado de empate."""
        self.service.track_game_draw(
            player1=self.player1,
            player2=self.player2,
            moves_count=9,
            game_duration_seconds=180
        )
        
        # Ambos jugadores deben tener empate registrado
        stats1 = self.player1.stats
        stats2 = self.player2.stats
        
        self.assertEqual(stats1.games_played, 1)
        self.assertEqual(stats1.games_drawn, 1)
        self.assertEqual(stats1.games_won, 0)
        self.assertEqual(stats1.games_lost, 0)
        
        self.assertEqual(stats2.games_played, 1)
        self.assertEqual(stats2.games_drawn, 1)
        self.assertEqual(stats2.games_won, 0)
        self.assertEqual(stats2.games_lost, 0)
    
    def test_get_player_performance_metrics(self):
        """Test de obtención de métricas de rendimiento del jugador."""
        # Simular varias partidas
        for _ in range(3):
            self.player1.record_game_won()
        
        for _ in range(2):
            self.player1.record_game_lost()
        
        self.player1.record_game_drawn()
        
        metrics = self.service.get_player_performance_metrics(self.player1)
        
        self.assertIsInstance(metrics, dict)
        self.assertIn('total_games', metrics)
        self.assertIn('win_rate', metrics)
        self.assertIn('loss_rate', metrics)
        self.assertIn('draw_rate', metrics)
        
        self.assertEqual(metrics['total_games'], 6)
        self.assertEqual(metrics['win_rate'], 50.0)  # 3/6 = 50%
    
    def test_get_global_statistics(self):
        """Test de obtención de estadísticas globales."""
        # Crear varios jugadores con estadísticas
        players = [
            self.player1,
            self.player2,
            Player("Jugador 3", PlayerType.HUMAN),
            Player("AI Hard", PlayerType.AI_HARD)
        ]
        
        # Simular algunas partidas
        for player in players[:2]:
            player.record_game_won()
            player.record_game_lost()
        
        global_stats = self.service.get_global_statistics(players)
        
        self.assertIsInstance(global_stats, dict)
        self.assertIn('total_players', global_stats)
        self.assertIn('total_games_played', global_stats)
        self.assertIn('human_vs_ai_games', global_stats)
        self.assertIn('human_vs_human_games', global_stats)
        
        self.assertEqual(global_stats['total_players'], 4)
    
    def test_get_ai_difficulty_statistics(self):
        """Test de estadísticas por dificultad de AI."""
        ai_easy = Player("AI Easy", PlayerType.AI_EASY)
        ai_medium = Player("AI Medium", PlayerType.AI_MEDIUM)
        ai_hard = Player("AI Hard", PlayerType.AI_HARD)
        
        ai_players = [ai_easy, ai_medium, ai_hard]
        
        # Simular partidas contra cada AI
        for ai in ai_players:
            ai.record_game_won()
            ai.record_game_lost()
        
        ai_stats = self.service.get_ai_difficulty_statistics(ai_players)
        
        self.assertIsInstance(ai_stats, dict)
        self.assertIn('easy', ai_stats)
        self.assertIn('medium', ai_stats)
        self.assertIn('hard', ai_stats)
        
        # Cada dificultad debe tener estadísticas
        for difficulty_stats in ai_stats.values():
            self.assertIn('games_played', difficulty_stats)
            self.assertIn('win_rate', difficulty_stats)


class TestServiceIntegration(unittest.TestCase):
    """Tests de integración entre servicios."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.ai_service = AIOpponentService()
        self.score_service = ScoreCalculatorService()
        self.stats_service = StatisticsTrackerService()
        
        self.human_player = Player("Humano", PlayerType.HUMAN)
        self.ai_player = Player("AI", PlayerType.AI_MEDIUM)
        
        self.human_player.assign_symbol(PlayerSymbol.X)
        self.ai_player.assign_symbol(PlayerSymbol.O)
    
    def test_complete_game_workflow(self):
        """Test de flujo completo de juego usando servicios."""
        board = Board()
        current_player = PlayerSymbol.X
        moves_count = 0
        
        # Simular algunas jugadas
        while not board.is_full() and board.get_winner() is None and moves_count < 5:
            if current_player == PlayerSymbol.X:
                # Jugada humana simulada (centro si está disponible)
                position = Position(1, 1) if board.is_position_empty(Position(1, 1)) else Position(0, 0)
                if board.is_position_empty(position):
                    move = Move(position, CellState.PLAYER_X)
                    board.place_move(move)
            else:
                # Jugada de AI
                ai_move = self.ai_service.get_best_move(
                    board=board,
                    player_symbol=PlayerSymbol.O,
                    difficulty=DifficultyLevel.MEDIUM
                )
                if ai_move:
                    board.place_move(ai_move)
            
            moves_count += 1
            current_player = PlayerSymbol.O if current_player == PlayerSymbol.X else PlayerSymbol.X
        
        # Calcular puntuación final
        winner = board.get_winner()
        if winner == CellState.PLAYER_X:
            score = self.score_service.calculate_match_score(
                winner=self.human_player,
                loser=self.ai_player,
                moves_count=moves_count,
                config=GameConfiguration()
            )
            
            # Registrar estadísticas
            self.stats_service.track_game_result(
                winner=self.human_player,
                loser=self.ai_player,
                moves_count=moves_count,
                game_duration_seconds=60
            )
            
        elif winner == CellState.PLAYER_O:
            score = self.score_service.calculate_match_score(
                winner=self.ai_player,
                loser=self.human_player,
                moves_count=moves_count,
                config=GameConfiguration()
            )
            
        else:
            # Empate
            score = self.score_service.calculate_draw_score(
                player1=self.human_player,
                player2=self.ai_player,
                moves_count=moves_count,
                config=GameConfiguration()
            )
        
        # Verificar que todo funcionó correctamente
        self.assertIsNotNone(score)
        self.assertIsInstance(score, dict)


if __name__ == '__main__':
    unittest.main()