"""
Entidad Board - Tablero de Tres en Raya.

Esta entidad representa el concepto central del tablero de juego en el dominio.
Se enfoca únicamente en el estado y comportamientos intrínsecos del tablero,
sin depender de implementaciones técnicas específicas.
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class CellState(Enum):
    """Estados posibles de una celda del tablero."""
    EMPTY = " "
    PLAYER_X = "X"
    PLAYER_O = "O"


class BoardSize(Enum):
    """Tamaños válidos del tablero."""
    STANDARD = 3  # 3x3 es el estándar para Tres en Raya


@dataclass(frozen=True)
class Position:
    """Representa una posición en el tablero."""
    row: int
    col: int
    
    def __post_init__(self):
        """Validar que la posición esté dentro de los límites válidos."""
        if not (0 <= self.row < BoardSize.STANDARD.value):
            raise ValueError(f"Fila debe estar entre 0 y {BoardSize.STANDARD.value - 1}")
        if not (0 <= self.col < BoardSize.STANDARD.value):
            raise ValueError(f"Columna debe estar entre 0 y {BoardSize.STANDARD.value - 1}")


@dataclass(frozen=True)
class Move:
    """Representa un movimiento en el juego."""
    position: Position
    player: CellState
    
    def __post_init__(self):
        """Validar que el jugador sea válido."""
        if self.player not in [CellState.PLAYER_X, CellState.PLAYER_O]:
            raise ValueError("El jugador debe ser X o O")


class Board:
    """
    Entidad Board - Representa el tablero del juego Tres en Raya.
    
    Esta es la entidad central que encapsula todas las reglas de negocio
    relacionadas con el estado y comportamiento del tablero.
    
    Principios de Screaming Architecture aplicados:
    - Se enfoca en el DOMINIO: Tablero de Tres en Raya
    - No depende de frameworks o tecnologías específicas
    - Encapsula las reglas de negocio del tablero
    - Utiliza Value Objects (Position, Move) para mayor expresividad
    """
    
    def __init__(self, size: BoardSize = BoardSize.STANDARD):
        """
        Inicializa un nuevo tablero vacío.
        
        Args:
            size: Tamaño del tablero (por defecto 3x3)
        """
        self._size = size.value
        self._grid: List[List[CellState]] = [
            [CellState.EMPTY for _ in range(self._size)]
            for _ in range(self._size)
        ]
        self._move_history: List[Move] = []
    
    @property
    def size(self) -> int:
        """Obtiene el tamaño del tablero."""
        return self._size
    
    @property
    def move_history(self) -> List[Move]:
        """Obtiene el historial de movimientos."""
        return self._move_history.copy()
    
    def get_cell_state(self, position: Position) -> CellState:
        """
        Obtiene el estado de una celda específica.
        
        Args:
            position: Posición de la celda
            
        Returns:
            Estado de la celda
        """
        return self._grid[position.row][position.col]
    
    def is_position_empty(self, position: Position) -> bool:
        """
        Verifica si una posición está vacía.
        
        Args:
            position: Posición a verificar
            
        Returns:
            True si la posición está vacía, False en caso contrario
        """
        return self.get_cell_state(position) == CellState.EMPTY
    
    def place_move(self, move: Move) -> bool:
        """
        Coloca un movimiento en el tablero.
        
        Args:
            move: Movimiento a realizar
            
        Returns:
            True si el movimiento fue exitoso, False si la posición está ocupada
            
        Raises:
            ValueError: Si el movimiento no es válido
        """
        if not self.is_position_empty(move.position):
            return False
            
        self._grid[move.position.row][move.position.col] = move.player
        self._move_history.append(move)
        return True
    
    def get_winner(self) -> Optional[CellState]:
        """
        Determina si hay un ganador en el tablero actual.
        
        Returns:
            El jugador ganador (X o O) o None si no hay ganador
        """
        # Verificar filas
        for row in range(self._size):
            if self._check_line([self._grid[row][col] for col in range(self._size)]):
                return self._grid[row][0]
        
        # Verificar columnas
        for col in range(self._size):
            if self._check_line([self._grid[row][col] for row in range(self._size)]):
                return self._grid[0][col]
        
        # Verificar diagonal principal
        if self._check_line([self._grid[i][i] for i in range(self._size)]):
            return self._grid[0][0]
        
        # Verificar diagonal secundaria
        if self._check_line([self._grid[i][self._size - 1 - i] for i in range(self._size)]):
            return self._grid[0][self._size - 1]
        
        return None
    
    def _check_line(self, line: List[CellState]) -> bool:
        """
        Verifica si una línea contiene tres símbolos iguales (no vacíos).
        
        Args:
            line: Lista de estados de celda
            
        Returns:
            True si la línea es ganadora, False en caso contrario
        """
        return (
            len(set(line)) == 1 and 
            line[0] != CellState.EMPTY
        )
    
    def is_full(self) -> bool:
        """
        Verifica si el tablero está completamente lleno.
        
        Returns:
            True si todas las celdas están ocupadas, False en caso contrario
        """
        for row in range(self._size):
            for col in range(self._size):
                if self._grid[row][col] == CellState.EMPTY:
                    return False
        return True
    
    def is_game_over(self) -> bool:
        """
        Verifica si el juego ha terminado (hay ganador o tablero lleno).
        
        Returns:
            True si el juego terminó, False en caso contrario
        """
        return self.get_winner() is not None or self.is_full()
    
    def get_empty_positions(self) -> List[Position]:
        """
        Obtiene todas las posiciones vacías del tablero.
        
        Returns:
            Lista de posiciones vacías
        """
        empty_positions = []
        for row in range(self._size):
            for col in range(self._size):
                position = Position(row, col)
                if self.is_position_empty(position):
                    empty_positions.append(position)
        return empty_positions
    
    def reset(self) -> None:
        """Reinicia el tablero a su estado inicial vacío."""
        self._grid = [
            [CellState.EMPTY for _ in range(self._size)]
            for _ in range(self._size)
        ]
        self._move_history.clear()
    
    def to_list(self) -> List[List[str]]:
        """
        Convierte el tablero a una representación de lista para compatibilidad.
        
        Returns:
            Representación del tablero como lista de listas de strings
        """
        return [[cell.value for cell in row] for row in self._grid]
    
    def __str__(self) -> str:
        """Representación string del tablero para debug."""
        lines = []
        for row in self._grid:
            line = "|".join(cell.value for cell in row)
            lines.append(line)
            lines.append("-" * len(line))
        return "\\n".join(lines[:-1])  # Remover última línea separadora