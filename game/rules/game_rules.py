"""
GameRules - Reglas del juego Tres en Raya.

Este módulo encapsula todas las reglas fundamentales del juego,
definiendo qué movimientos son válidos y cómo se determina el resultado.
"""

from typing import List, Optional, Tuple
from enum import Enum

from game.entities import Board, Position, Move, CellState, Player, PlayerSymbol


class RuleViolationType(Enum):
    """Tipos de violación de reglas."""
    POSITION_OCCUPIED = "position_occupied"
    INVALID_POSITION = "invalid_position"
    WRONG_TURN = "wrong_turn"
    GAME_FINISHED = "game_finished"
    PLAYER_NOT_ASSIGNED = "player_not_assigned"


class RuleViolation(Exception):
    """Excepción para violaciones de reglas del juego."""
    
    def __init__(self, violation_type: RuleViolationType, message: str):
        """
        Inicializa una violación de regla.
        
        Args:
            violation_type: Tipo específico de violación
            message: Mensaje descriptivo del error
        """
        self.violation_type = violation_type
        self.message = message
        super().__init__(message)


class GameRules:
    """
    GameRules - Reglas fundamentales del juego Tres en Raya.
    
    Esta clase del dominio encapsula todas las reglas que gobiernan
    el juego de Tres en Raya, desde la validación de movimientos
    hasta la determinación de condiciones de victoria.
    
    Principios de Screaming Architecture aplicados:
    - Se enfoca en el DOMINIO: Reglas del juego Tres en Raya
    - Encapsula la lógica de validación del juego
    - Define qué constituye un juego válido
    - No depende de tecnologías específicas
    """
    
    # Constantes del juego
    BOARD_SIZE = 3
    MIN_MOVES_FOR_WIN = 5  # Mínimo de movimientos totales para que sea posible ganar
    MAX_MOVES = 9  # Máximo de movimientos posibles en el tablero
    
    def __init__(self):
        """Inicializa las reglas del juego."""
        pass
    
    def validate_move(self, board: Board, move: Move, current_player: Player) -> None:
        """
        Valida si un movimiento es legal según las reglas del juego.
        
        Args:
            board: Estado actual del tablero
            move: Movimiento a validar
            current_player: Jugador que intenta realizar el movimiento
            
        Raises:
            RuleViolation: Si el movimiento viola alguna regla
        """
        # 1. Verificar que el jugador tenga símbolo asignado
        if not current_player.symbol:
            raise RuleViolation(
                RuleViolationType.PLAYER_NOT_ASSIGNED,
                f"El jugador {current_player.name} no tiene símbolo asignado"
            )
        
        # 2. Verificar que la posición esté dentro del tablero
        if not self._is_valid_position(move.position):
            raise RuleViolation(
                RuleViolationType.INVALID_POSITION,
                f"La posición {move.position} está fuera del tablero"
            )
        
        # 3. Verificar que la posición esté libre
        if not board.is_position_empty(move.position):
            raise RuleViolation(
                RuleViolationType.POSITION_OCCUPIED,
                f"La posición {move.position} ya está ocupada"
            )
        
        # 4. Verificar que el movimiento corresponda al jugador correcto
        expected_cell_state = self._player_symbol_to_cell_state(current_player.symbol)
        if move.player != expected_cell_state:
            raise RuleViolation(
                RuleViolationType.WRONG_TURN,
                f"El movimiento no corresponde al símbolo del jugador {current_player.name}"
            )
        
        # 5. Verificar que el juego no haya terminado
        if board.get_winner() is not None or board.is_full():
            raise RuleViolation(
                RuleViolationType.GAME_FINISHED,
                "No se pueden realizar movimientos en un juego terminado"
            )
    
    def is_game_finished(self, board: Board) -> bool:
        """
        Determina si el juego ha terminado.
        
        Args:
            board: Estado actual del tablero
            
        Returns:
            True si el juego ha terminado, False en caso contrario
        """
        return board.get_winner() is not None or board.is_full()
    
    def get_winner(self, board: Board) -> Optional[CellState]:
        """
        Determina el ganador del juego según las reglas.
        
        Args:
            board: Estado actual del tablero
            
        Returns:
            CellState del ganador o None si no hay ganador
        """
        return board.get_winner()
    
    def is_draw(self, board: Board) -> bool:
        """
        Determina si el juego ha terminado en empate.
        
        Args:
            board: Estado actual del tablero
            
        Returns:
            True si es empate, False en caso contrario
        """
        return board.is_full() and board.get_winner() is None
    
    def get_valid_moves(self, board: Board) -> List[Position]:
        """
        Obtiene todas las posiciones válidas para el próximo movimiento.
        
        Args:
            board: Estado actual del tablero
            
        Returns:
            Lista de posiciones válidas
        """
        if self.is_game_finished(board):
            return []
        
        return board.get_empty_positions()
    
    def can_player_move(self, board: Board, player: Player) -> bool:
        """
        Verifica si un jugador puede realizar un movimiento.
        
        Args:
            board: Estado actual del tablero
            player: Jugador a verificar
            
        Returns:
            True si el jugador puede mover, False en caso contrario
        """
        # Verificar que el juego no haya terminado
        if self.is_game_finished(board):
            return False
        
        # Verificar que el jugador tenga símbolo asignado
        if not player.symbol:
            return False
        
        # Verificar que haya posiciones disponibles
        return len(self.get_valid_moves(board)) > 0
    
    def get_next_player_symbol(self, board: Board) -> PlayerSymbol:
        """
        Determina qué símbolo debe jugar a continuación.
        
        Args:
            board: Estado actual del tablero
            
        Returns:
            Símbolo del siguiente jugador
        """
        move_count = self._count_moves(board)
        
        # X siempre empieza
        if move_count % 2 == 0:
            return PlayerSymbol.X
        else:
            return PlayerSymbol.O
    
    def is_player_turn(self, board: Board, player: Player) -> bool:
        """
        Verifica si es el turno de un jugador específico.
        
        Args:
            board: Estado actual del tablero
            player: Jugador a verificar
            
        Returns:
            True si es el turno del jugador, False en caso contrario
        """
        if not player.symbol:
            return False
        
        next_symbol = self.get_next_player_symbol(board)
        return player.symbol == next_symbol
    
    def validate_game_setup(self, player1: Player, player2: Player) -> None:
        """
        Valida que la configuración del juego sea correcta.
        
        Args:
            player1: Primer jugador
            player2: Segundo jugador
            
        Raises:
            RuleViolation: Si la configuración no es válida
        """
        # Verificar que los jugadores sean diferentes
        if player1.id == player2.id:
            raise RuleViolation(
                RuleViolationType.PLAYER_NOT_ASSIGNED,
                "No se puede jugar contra uno mismo"
            )
        
        # Verificar que ambos jugadores tengan símbolos asignados
        if not player1.symbol or not player2.symbol:
            raise RuleViolation(
                RuleViolationType.PLAYER_NOT_ASSIGNED,
                "Ambos jugadores deben tener símbolos asignados"
            )
        
        # Verificar que tengan símbolos diferentes
        if player1.symbol == player2.symbol:
            raise RuleViolation(
                RuleViolationType.PLAYER_NOT_ASSIGNED,
                "Los jugadores deben tener símbolos diferentes"
            )
        
        # Verificar que los símbolos sean válidos
        valid_symbols = {PlayerSymbol.X, PlayerSymbol.O}
        if player1.symbol not in valid_symbols or player2.symbol not in valid_symbols:
            raise RuleViolation(
                RuleViolationType.PLAYER_NOT_ASSIGNED,
                "Los símbolos deben ser X u O"
            )
    
    def calculate_move_number(self, board: Board) -> int:
        """
        Calcula el número de movimiento actual (1-based).
        
        Args:
            board: Estado actual del tablero
            
        Returns:
            Número del próximo movimiento
        """
        return self._count_moves(board) + 1
    
    def is_winning_move(self, board: Board, move: Move) -> bool:
        """
        Determina si un movimiento específico resulta en victoria.
        
        Args:
            board: Estado actual del tablero
            move: Movimiento a evaluar
            
        Returns:
            True si el movimiento gana el juego, False en caso contrario
        """
        # Crear copia del tablero para simular
        temp_board = self._copy_board(board)
        
        try:
            temp_board.place_move(move)
            return temp_board.get_winner() == move.player
        except Exception:
            return False
    
    def get_winning_positions(self, board: Board, player_symbol: PlayerSymbol) -> List[Position]:
        """
        Obtiene todas las posiciones que resultarían en victoria inmediata.
        
        Args:
            board: Estado actual del tablero
            player_symbol: Símbolo del jugador
            
        Returns:
            Lista de posiciones ganadoras
        """
        winning_positions = []
        cell_state = self._player_symbol_to_cell_state(player_symbol)
        
        for position in self.get_valid_moves(board):
            move = Move(position=position, player=cell_state)
            if self.is_winning_move(board, move):
                winning_positions.append(position)
        
        return winning_positions
    
    def get_blocking_positions(self, board: Board, opponent_symbol: PlayerSymbol) -> List[Position]:
        """
        Obtiene posiciones que bloquean la victoria del oponente.
        
        Args:
            board: Estado actual del tablero
            opponent_symbol: Símbolo del oponente
            
        Returns:
            Lista de posiciones que bloquean al oponente
        """
        return self.get_winning_positions(board, opponent_symbol)
    
    def _is_valid_position(self, position: Position) -> bool:
        """
        Verifica si una posición está dentro de los límites del tablero.
        
        Args:
            position: Posición a verificar
            
        Returns:
            True si la posición es válida, False en caso contrario
        """
        return (
            0 <= position.row < self.BOARD_SIZE and
            0 <= position.col < self.BOARD_SIZE
        )
    
    def _player_symbol_to_cell_state(self, symbol: PlayerSymbol) -> CellState:
        """
        Convierte un símbolo de jugador a estado de celda.
        
        Args:
            symbol: Símbolo del jugador
            
        Returns:
            Estado de celda correspondiente
        """
        if symbol == PlayerSymbol.X:
            return CellState.PLAYER_X
        elif symbol == PlayerSymbol.O:
            return CellState.PLAYER_O
        else:
            raise ValueError(f"Símbolo de jugador inválido: {symbol}")
    
    def _count_moves(self, board: Board) -> int:
        """
        Cuenta el número de movimientos realizados en el tablero.
        
        Args:
            board: Tablero a analizar
            
        Returns:
            Número de movimientos realizados
        """
        count = 0
        board_list = board.to_list()
        
        for row in board_list:
            for cell in row:
                if cell != ' ':  # Celda ocupada
                    count += 1
        
        return count
    
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
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                cell_value = board_list[row][col]
                if cell_value != ' ':
                    cell_state = CellState.PLAYER_X if cell_value == 'X' else CellState.PLAYER_O
                    position = Position(row, col)
                    move = Move(position=position, player=cell_state)
                    new_board.place_move(move)
        
        return new_board