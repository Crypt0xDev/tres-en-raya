"""
Servicio AIOpponent - Oponente de Inteligencia Artificial para Tres en Raya.

Este servicio implementa diferentes estrategias de IA para jugar contra
jugadores humanos, encapsulando la lógica de toma de decisiones.
"""

import random
from typing import List, Optional, Tuple
from enum import Enum

from game.entities import Board, Position, CellState, Player, PlayerType, PlayerSymbol


class AIStrategy(Enum):
    """Estrategias disponibles para la IA."""
    RANDOM = "random"
    DEFENSIVE = "defensive"
    AGGRESSIVE = "aggressive"
    MINIMAX = "minimax"


class AIDifficulty(Enum):
    """Niveles de dificultad de la IA."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class AIOpponent:
    """
    Servicio AIOpponent - Oponente de inteligencia artificial.
    
    Este servicio del dominio encapsula toda la lógica relacionada con
    la inteligencia artificial del juego, proporcionando diferentes
    niveles de dificultad y estrategias.
    
    Principios de Screaming Architecture aplicados:
    - Se enfoca en el DOMINIO: IA para Tres en Raya
    - Encapsula estrategias de juego inteligente
    - No depende de frameworks externos
    - Utiliza entidades del dominio
    """
    
    def __init__(self, difficulty: AIDifficulty = AIDifficulty.MEDIUM):
        """
        Inicializa el oponente IA.
        
        Args:
            difficulty: Nivel de dificultad de la IA
        """
        self._difficulty = difficulty
        self._strategy_map = {
            AIDifficulty.EASY: AIStrategy.RANDOM,
            AIDifficulty.MEDIUM: AIStrategy.DEFENSIVE,
            AIDifficulty.HARD: AIStrategy.MINIMAX
        }
    
    def get_best_move(self, board: Board, ai_player: Player) -> Optional[Position]:
        """
        Obtiene el mejor movimiento para el jugador IA.
        
        Args:
            board: Estado actual del tablero
            ai_player: Jugador IA que debe mover
            
        Returns:
            Mejor posición para mover o None si no hay movimientos disponibles
        """
        available_positions = board.get_empty_positions()
        
        if not available_positions:
            return None
        
        if not ai_player.symbol:
            return None
        
        # Seleccionar estrategia basada en dificultad
        strategy = self._strategy_map[self._difficulty]
        
        if strategy == AIStrategy.RANDOM:
            return self._get_random_move(available_positions)
        elif strategy == AIStrategy.DEFENSIVE:
            return self._get_defensive_move(board, ai_player, available_positions)
        elif strategy == AIStrategy.AGGRESSIVE:
            return self._get_aggressive_move(board, ai_player, available_positions)
        elif strategy == AIStrategy.MINIMAX:
            return self._get_minimax_move(board, ai_player, available_positions)
        else:
            return self._get_random_move(available_positions)
    
    def _get_random_move(self, available_positions: List[Position]) -> Position:
        """
        Estrategia aleatoria - selecciona una posición al azar.
        
        Args:
            available_positions: Posiciones disponibles
            
        Returns:
            Posición seleccionada aleatoriamente
        """
        return random.choice(available_positions)
    
    def _get_defensive_move(
        self, 
        board: Board, 
        ai_player: Player, 
        available_positions: List[Position]
    ) -> Position:
        """
        Estrategia defensiva - prioriza bloquear al oponente.
        
        Args:
            board: Estado del tablero
            ai_player: Jugador IA
            available_positions: Posiciones disponibles
            
        Returns:
            Mejor posición defensiva
        """
        # 1. Si puede ganar, ganar
        winning_move = self._find_winning_move(board, ai_player, available_positions)
        if winning_move:
            return winning_move
        
        # 2. Si el oponente puede ganar, bloquear
        opponent_symbol = PlayerSymbol.X if ai_player.symbol == PlayerSymbol.O else PlayerSymbol.O
        blocking_move = self._find_blocking_move(board, opponent_symbol, available_positions)
        if blocking_move:
            return blocking_move
        
        # 3. Tomar el centro si está disponible
        center = Position(1, 1)
        if center in available_positions:
            return center
        
        # 4. Tomar una esquina
        corners = [Position(0, 0), Position(0, 2), Position(2, 0), Position(2, 2)]
        available_corners = [pos for pos in corners if pos in available_positions]
        if available_corners:
            return random.choice(available_corners)
        
        # 5. Movimiento aleatorio
        return self._get_random_move(available_positions)
    
    def _get_aggressive_move(
        self, 
        board: Board, 
        ai_player: Player, 
        available_positions: List[Position]
    ) -> Position:
        """
        Estrategia agresiva - prioriza crear oportunidades de victoria.
        
        Args:
            board: Estado del tablero
            ai_player: Jugador IA
            available_positions: Posiciones disponibles
            
        Returns:
            Mejor posición agresiva
        """
        # 1. Si puede ganar, ganar
        winning_move = self._find_winning_move(board, ai_player, available_positions)
        if winning_move:
            return winning_move
        
        # 2. Crear oportunidades de doble amenaza
        best_tactical_move = self._find_tactical_move(board, ai_player, available_positions)
        if best_tactical_move:
            return best_tactical_move
        
        # 3. Si el oponente puede ganar, bloquear
        opponent_symbol = PlayerSymbol.X if ai_player.symbol == PlayerSymbol.O else PlayerSymbol.O
        blocking_move = self._find_blocking_move(board, opponent_symbol, available_positions)
        if blocking_move:
            return blocking_move
        
        # 4. Movimiento defensivo
        return self._get_defensive_move(board, ai_player, available_positions)
    
    def _get_minimax_move(
        self, 
        board: Board, 
        ai_player: Player, 
        available_positions: List[Position]
    ) -> Position:
        """
        Estrategia minimax - algoritmo perfecto.
        
        Args:
            board: Estado del tablero
            ai_player: Jugador IA
            available_positions: Posiciones disponibles
            
        Returns:
            Mejor posición según minimax
        """
        if not ai_player.symbol:
            return self._get_random_move(available_positions)
        
        best_score = float('-inf')
        best_move = available_positions[0]
        
        ai_cell_state = CellState.PLAYER_X if ai_player.symbol == PlayerSymbol.X else CellState.PLAYER_O
        opponent_cell_state = CellState.PLAYER_O if ai_cell_state == CellState.PLAYER_X else CellState.PLAYER_X
        
        for position in available_positions:
            # Simular movimiento
            from game.entities import Move
            move = Move(position=position, player=ai_cell_state)
            
            # Crear copia del tablero para simular
            board_copy = self._copy_board(board)
            board_copy.place_move(move)
            
            # Evaluar con minimax
            score = self._minimax(board_copy, 0, False, ai_cell_state, opponent_cell_state)
            
            if score > best_score:
                best_score = score
                best_move = position
        
        return best_move
    
    def _minimax(
        self, 
        board: Board, 
        depth: int, 
        is_maximizing: bool,
        ai_cell_state: CellState,
        opponent_cell_state: CellState
    ) -> float:
        """
        Algoritmo minimax recursivo.
        
        Args:
            board: Estado del tablero
            depth: Profundidad actual
            is_maximizing: Si es turno del maximizador (IA)
            ai_cell_state: Estado de celda de la IA
            opponent_cell_state: Estado de celda del oponente
            
        Returns:
            Puntuación del movimiento
        """
        # Verificar condiciones de parada
        winner = board.get_winner()
        
        if winner == ai_cell_state:
            return 10 - depth  # IA gana (preferir victoria rápida)
        elif winner == opponent_cell_state:
            return depth - 10  # Oponente gana (preferir derrota tardía)
        elif board.is_full():
            return 0  # Empate
        
        available_positions = board.get_empty_positions()
        
        if is_maximizing:
            best_score = float('-inf')
            for position in available_positions:
                # Simular movimiento de IA
                from game.entities import Move
                move = Move(position=position, player=ai_cell_state)
                board_copy = self._copy_board(board)
                board_copy.place_move(move)
                
                score = self._minimax(board_copy, depth + 1, False, ai_cell_state, opponent_cell_state)
                best_score = max(score, best_score)
            
            return best_score
        else:
            best_score = float('inf')
            for position in available_positions:
                # Simular movimiento del oponente
                from game.entities import Move
                move = Move(position=position, player=opponent_cell_state)
                board_copy = self._copy_board(board)
                board_copy.place_move(move)
                
                score = self._minimax(board_copy, depth + 1, True, ai_cell_state, opponent_cell_state)
                best_score = min(score, best_score)
            
            return best_score
    
    def _find_winning_move(
        self, 
        board: Board, 
        player: Player, 
        available_positions: List[Position]
    ) -> Optional[Position]:
        """
        Busca un movimiento que resulte en victoria inmediata.
        
        Args:
            board: Estado del tablero
            player: Jugador que busca ganar
            available_positions: Posiciones disponibles
            
        Returns:
            Posición ganadora o None si no existe
        """
        if not player.symbol:
            return None
        
        player_cell_state = CellState.PLAYER_X if player.symbol == PlayerSymbol.X else CellState.PLAYER_O
        
        for position in available_positions:
            # Simular movimiento
            from game.entities import Move
            move = Move(position=position, player=player_cell_state)
            board_copy = self._copy_board(board)
            board_copy.place_move(move)
            
            # Verificar si gana
            if board_copy.get_winner() == player_cell_state:
                return position
        
        return None
    
    def _find_blocking_move(
        self, 
        board: Board, 
        opponent_symbol: PlayerSymbol, 
        available_positions: List[Position]
    ) -> Optional[Position]:
        """
        Busca un movimiento que bloquee la victoria del oponente.
        
        Args:
            board: Estado del tablero
            opponent_symbol: Símbolo del oponente
            available_positions: Posiciones disponibles
            
        Returns:
            Posición que bloquea o None si no es necesario
        """
        opponent_cell_state = CellState.PLAYER_X if opponent_symbol == PlayerSymbol.X else CellState.PLAYER_O
        
        for position in available_positions:
            # Simular movimiento del oponente
            from game.entities import Move
            move = Move(position=position, player=opponent_cell_state)
            board_copy = self._copy_board(board)
            board_copy.place_move(move)
            
            # Verificar si el oponente ganaría
            if board_copy.get_winner() == opponent_cell_state:
                return position
        
        return None
    
    def _find_tactical_move(
        self, 
        board: Board, 
        player: Player, 
        available_positions: List[Position]
    ) -> Optional[Position]:
        """
        Busca movimientos tácticos que creen múltiples amenazas.
        
        Args:
            board: Estado del tablero
            player: Jugador IA
            available_positions: Posiciones disponibles
            
        Returns:
            Mejor movimiento táctico o None
        """
        # Implementación básica: buscar posiciones que creen dos líneas con dos marcas
        # Esta es una simplificación - en una implementación completa se analizarían
        # todas las combinaciones posibles de amenazas
        
        best_position = None
        max_threats = 0
        
        if not player.symbol:
            return None
        
        player_cell_state = CellState.PLAYER_X if player.symbol == PlayerSymbol.X else CellState.PLAYER_O
        
        for position in available_positions:
            threat_count = self._count_potential_threats(board, position, player_cell_state)
            if threat_count > max_threats:
                max_threats = threat_count
                best_position = position
        
        return best_position if max_threats > 1 else None
    
    def _count_potential_threats(self, board: Board, position: Position, player_cell_state: CellState) -> int:
        """
        Cuenta las amenazas potenciales que se crearían con un movimiento.
        
        Args:
            board: Estado del tablero
            position: Posición a evaluar
            player_cell_state: Estado de celda del jugador
            
        Returns:
            Número de amenazas potenciales
        """
        # Simular colocación
        from game.entities import Move
        move = Move(position=position, player=player_cell_state)
        board_copy = self._copy_board(board)
        board_copy.place_move(move)
        
        threats = 0
        
        # Verificar líneas que ahora tienen 2 marcas del jugador
        board_list = board_copy.to_list()
        player_symbol = player_cell_state.value
        
        # Verificar filas
        for row in range(3):
            if board_list[row].count(player_symbol) == 2 and board_list[row].count(' ') == 1:
                threats += 1
        
        # Verificar columnas
        for col in range(3):
            column = [board_list[row][col] for row in range(3)]
            if column.count(player_symbol) == 2 and column.count(' ') == 1:
                threats += 1
        
        # Verificar diagonales
        diagonal1 = [board_list[i][i] for i in range(3)]
        if diagonal1.count(player_symbol) == 2 and diagonal1.count(' ') == 1:
            threats += 1
        
        diagonal2 = [board_list[i][2-i] for i in range(3)]
        if diagonal2.count(player_symbol) == 2 and diagonal2.count(' ') == 1:
            threats += 1
        
        return threats
    
    def _copy_board(self, board: Board) -> Board:
        """
        Crea una copia del tablero para simulaciones.
        
        Args:
            board: Tablero original
            
        Returns:
            Copia del tablero
        """
        new_board = Board()
        new_board.reset()
        
        # Copiar estado actual
        board_list = board.to_list()
        for row in range(3):
            for col in range(3):
                if board_list[row][col] != ' ':
                    cell_state = CellState.PLAYER_X if board_list[row][col] == 'X' else CellState.PLAYER_O
                    position = Position(row, col)
                    from game.entities import Move
                    move = Move(position=position, player=cell_state)
                    new_board.place_move(move)
        
        return new_board