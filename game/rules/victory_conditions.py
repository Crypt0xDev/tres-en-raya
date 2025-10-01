"""
VictoryConditions - Condiciones de victoria del juego Tres en Raya.

Este módulo define todas las condiciones que determinan cuándo
y cómo se gana una partida de Tres en Raya.
"""

from typing import List, Optional, Tuple, Set, Dict
from enum import Enum
from dataclasses import dataclass

from game.entities import Board, Position, CellState


class VictoryType(Enum):
    """Tipos de victoria en Tres en Raya."""
    HORIZONTAL_LINE = "horizontal_line"
    VERTICAL_LINE = "vertical_line"
    DIAGONAL_LINE = "diagonal_line"
    NO_VICTORY = "no_victory"


@dataclass(frozen=True)
class VictoryPattern:
    """Patrón de victoria inmutable."""
    victory_type: VictoryType
    winning_positions: Tuple[Position, ...]
    winner: CellState
    
    def __post_init__(self):
        """Validación post-inicialización."""
        if len(self.winning_positions) != 3:
            raise ValueError("Un patrón de victoria debe tener exactamente 3 posiciones")


class VictoryConditions:
    """
    VictoryConditions - Condiciones de victoria del dominio.
    
    Esta clase del dominio encapsula toda la lógica relacionada con
    la detección y validación de condiciones de victoria en el
    juego de Tres en Raya.
    
    Principios de Screaming Architecture aplicados:
    - Se enfoca en el DOMINIO: Condiciones de victoria en Tres en Raya
    - Encapsula la lógica de detección de patrones ganadores
    - Define qué constituye una victoria válida
    - No depende de tecnologías específicas
    """
    
    # Patrones de líneas ganadoras (posiciones del tablero 3x3)
    WINNING_LINES = [
        # Filas horizontales
        [(0, 0), (0, 1), (0, 2)],  # Fila superior
        [(1, 0), (1, 1), (1, 2)],  # Fila media
        [(2, 0), (2, 1), (2, 2)],  # Fila inferior
        
        # Columnas verticales
        [(0, 0), (1, 0), (2, 0)],  # Columna izquierda
        [(0, 1), (1, 1), (2, 1)],  # Columna central
        [(0, 2), (1, 2), (2, 2)],  # Columna derecha
        
        # Diagonales
        [(0, 0), (1, 1), (2, 2)],  # Diagonal principal
        [(0, 2), (1, 1), (2, 0)],  # Diagonal secundaria
    ]
    
    def __init__(self):
        """Inicializa las condiciones de victoria."""
        pass
    
    def check_victory(self, board: Board) -> Optional[VictoryPattern]:
        """
        Verifica si hay una condición de victoria en el tablero.
        
        Args:
            board: Estado actual del tablero
            
        Returns:
            VictoryPattern si hay victoria, None si no la hay
        """
        board_state = board.to_list()
        
        for line_positions in self.WINNING_LINES:
            victory_pattern = self._check_line(board_state, line_positions)
            if victory_pattern:
                return victory_pattern
        
        return None
    
    def has_winner(self, board: Board) -> bool:
        """
        Verifica rápidamente si hay un ganador.
        
        Args:
            board: Estado actual del tablero
            
        Returns:
            True si hay ganador, False en caso contrario
        """
        return self.check_victory(board) is not None
    
    def get_winner(self, board: Board) -> Optional[CellState]:
        """
        Obtiene el ganador del tablero.
        
        Args:
            board: Estado actual del tablero
            
        Returns:
            CellState del ganador o None si no hay ganador
        """
        victory_pattern = self.check_victory(board)
        return victory_pattern.winner if victory_pattern else None
    
    def get_winning_line(self, board: Board) -> Optional[List[Position]]:
        """
        Obtiene las posiciones de la línea ganadora.
        
        Args:
            board: Estado actual del tablero
            
        Returns:
            Lista de posiciones ganadoras o None si no hay victoria
        """
        victory_pattern = self.check_victory(board)
        return list(victory_pattern.winning_positions) if victory_pattern else None
    
    def is_potential_winning_line(self, board: Board, line_positions: List[Tuple[int, int]]) -> bool:
        """
        Verifica si una línea tiene potencial de victoria.
        
        Una línea tiene potencial si tiene al menos una marca del mismo jugador
        y el resto de posiciones están vacías.
        
        Args:
            board: Estado actual del tablero
            line_positions: Posiciones de la línea a verificar
            
        Returns:
            True si la línea tiene potencial, False en caso contrario
        """
        board_state = board.to_list()
        line_values = [board_state[row][col] for row, col in line_positions]
        
        # Contar marcas de cada tipo
        x_count = line_values.count('X')
        o_count = line_values.count('O')
        empty_count = line_values.count(' ')
        
        # Línea tiene potencial si solo tiene marcas de un jugador y espacios vacíos
        return (x_count > 0 and o_count == 0) or (o_count > 0 and x_count == 0)
    
    def count_potential_wins(self, board: Board, player_state: CellState) -> int:
        """
        Cuenta cuántas líneas tienen potencial de victoria para un jugador.
        
        Args:
            board: Estado actual del tablero
            player_state: Estado del jugador (X o O)
            
        Returns:
            Número de líneas con potencial de victoria
        """
        board_state = board.to_list()
        player_symbol = player_state.value
        count = 0
        
        for line_positions in self.WINNING_LINES:
            line_values = [board_state[row][col] for row, col in line_positions]
            
            # Verificar si la línea tiene solo marcas del jugador y espacios vacíos
            has_player_mark = player_symbol in line_values
            has_opponent_mark = any(
                val != ' ' and val != player_symbol for val in line_values
            )
            
            if has_player_mark and not has_opponent_mark:
                count += 1
        
        return count
    
    def get_threats(self, board: Board, player_state: CellState) -> List[Position]:
        """
        Obtiene posiciones que representan amenazas inmediatas de victoria.
        
        Una amenaza es una línea con dos marcas del jugador y un espacio vacío.
        
        Args:
            board: Estado actual del tablero
            player_state: Estado del jugador
            
        Returns:
            Lista de posiciones que completan amenazas
        """
        threats = []
        board_state = board.to_list()
        player_symbol = player_state.value
        
        for line_positions in self.WINNING_LINES:
            line_values = [board_state[row][col] for row, col in line_positions]
            
            # Verificar si hay exactamente 2 marcas del jugador y 1 espacio vacío
            player_count = line_values.count(player_symbol)
            empty_count = line_values.count(' ')
            
            if player_count == 2 and empty_count == 1:
                # Encontrar la posición vacía
                for i, (row, col) in enumerate(line_positions):
                    if line_values[i] == ' ':
                        threats.append(Position(row, col))
                        break
        
        return threats
    
    def get_blocks_needed(self, board: Board, opponent_state: CellState) -> List[Position]:
        """
        Obtiene posiciones donde se debe bloquear al oponente.
        
        Args:
            board: Estado actual del tablero
            opponent_state: Estado del oponente
            
        Returns:
            Lista de posiciones críticas para bloquear
        """
        return self.get_threats(board, opponent_state)
    
    def analyze_board_control(self, board: Board) -> Dict[str, int]:
        """
        Analiza el control del tablero por cada jugador.
        
        Args:
            board: Estado actual del tablero
            
        Returns:
            Diccionario con métricas de control del tablero
        """
        x_potential = self.count_potential_wins(board, CellState.PLAYER_X)
        o_potential = self.count_potential_wins(board, CellState.PLAYER_O)
        
        x_threats = len(self.get_threats(board, CellState.PLAYER_X))
        o_threats = len(self.get_threats(board, CellState.PLAYER_O))
        
        return {
            "x_potential_lines": x_potential,
            "o_potential_lines": o_potential,
            "x_immediate_threats": x_threats,
            "o_immediate_threats": o_threats,
            "control_advantage": x_potential - o_potential,
            "threat_advantage": x_threats - o_threats
        }
    
    def is_fork_opportunity(self, board: Board, position: Position, player_state: CellState) -> bool:
        """
        Verifica si una posición crea una oportunidad de fork (doble amenaza).
        
        Args:
            board: Estado actual del tablero
            position: Posición a evaluar
            player_state: Estado del jugador
            
        Returns:
            True si la posición crea un fork, False en caso contrario
        """
        # Simular colocación de la marca
        from game.entities import Move
        
        # Crear copia del tablero
        temp_board = self._copy_board(board)
        move = Move(position=position, player=player_state)
        
        try:
            temp_board.place_move(move)
            
            # Contar amenazas después del movimiento
            threats_after = self.get_threats(temp_board, player_state)
            
            # Fork si hay 2 o más amenazas
            return len(threats_after) >= 2
            
        except Exception:
            return False
    
    def get_fork_positions(self, board: Board, player_state: CellState) -> List[Position]:
        """
        Obtiene todas las posiciones que crean oportunidades de fork.
        
        Args:
            board: Estado actual del tablero
            player_state: Estado del jugador
            
        Returns:
            Lista de posiciones que crean forks
        """
        fork_positions = []
        
        for position in board.get_empty_positions():
            if self.is_fork_opportunity(board, position, player_state):
                fork_positions.append(position)
        
        return fork_positions
    
    def _check_line(self, board_state: List[List[str]], line_positions: List[Tuple[int, int]]) -> Optional[VictoryPattern]:
        """
        Verifica si una línea específica contiene una victoria.
        
        Args:
            board_state: Estado del tablero como matriz
            line_positions: Posiciones de la línea a verificar
            
        Returns:
            VictoryPattern si hay victoria en esta línea, None en caso contrario
        """
        # Obtener valores de las posiciones
        line_values = [board_state[row][col] for row, col in line_positions]
        
        # Verificar si todos son iguales y no están vacíos
        if len(set(line_values)) == 1 and line_values[0] != ' ':
            # Determinar tipo de victoria
            victory_type = self._determine_victory_type(line_positions)
            
            # Determinar ganador
            winner = CellState.PLAYER_X if line_values[0] == 'X' else CellState.PLAYER_O
            
            # Convertir posiciones a objetos Position
            positions = tuple(Position(row, col) for row, col in line_positions)
            
            return VictoryPattern(
                victory_type=victory_type,
                winning_positions=positions,
                winner=winner
            )
        
        return None
    
    def _determine_victory_type(self, line_positions: List[Tuple[int, int]]) -> VictoryType:
        """
        Determina el tipo de victoria basado en las posiciones.
        
        Args:
            line_positions: Posiciones de la línea ganadora
            
        Returns:
            Tipo de victoria
        """
        rows = [pos[0] for pos in line_positions]
        cols = [pos[1] for pos in line_positions]
        
        # Verificar si es línea horizontal (misma fila)
        if len(set(rows)) == 1:
            return VictoryType.HORIZONTAL_LINE
        
        # Verificar si es línea vertical (misma columna)
        if len(set(cols)) == 1:
            return VictoryType.VERTICAL_LINE
        
        # Si no es horizontal ni vertical, debe ser diagonal
        return VictoryType.DIAGONAL_LINE
    
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
                cell_value = board_list[row][col]
                if cell_value != ' ':
                    cell_state = CellState.PLAYER_X if cell_value == 'X' else CellState.PLAYER_O
                    position = Position(row, col)
                    from game.entities import Move
                    move = Move(position=position, player=cell_state)
                    new_board.place_move(move)
        
        return new_board