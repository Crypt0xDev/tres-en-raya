"""
Entidad GameSession - Sesión de juego de Tres en Raya.

Esta entidad representa una sesión completa de juego, encapsulando
el estado del juego, los jugadores participantes y el flujo del juego.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import uuid

from .board import Board, Move, Position, CellState
from .player import Player, PlayerSymbol


class GameState(Enum):
    """Estados posibles del juego."""
    WAITING_FOR_PLAYERS = "waiting_for_players"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    PAUSED = "paused"
    ABANDONED = "abandoned"


class GameResult(Enum):
    """Resultados posibles del juego."""
    PLAYER_X_WINS = "player_x_wins"
    PLAYER_O_WINS = "player_o_wins" 
    DRAW = "draw"
    ABANDONED = "abandoned"


@dataclass(frozen=True)
class GameConfiguration:
    """Configuración inmutable del juego."""
    board_size: int = 3
    max_players: int = 2
    allow_ai_players: bool = True
    time_limit_per_move: Optional[int] = None  # segundos
    enable_statistics: bool = True


class GameSession:
    """
    Entidad GameSession - Representa una sesión completa de juego Tres en Raya.
    
    Esta entidad coordina el estado completo de una partida, incluyendo
    el tablero, los jugadores, las reglas y el flujo del juego.
    
    Principios de Screaming Architecture aplicados:
    - Se enfoca en el DOMINIO: Sesión de juego de Tres en Raya
    - Encapsula las reglas de negocio del flujo de juego
    - Coordina las entidades Board y Player
    - No depende de tecnologías específicas
    """
    
    def __init__(
        self,
        configuration: GameConfiguration = GameConfiguration(),
        session_id: Optional[str] = None
    ):
        """
        Inicializa una nueva sesión de juego.
        
        Args:
            configuration: Configuración del juego
            session_id: ID único de la sesión (se genera automáticamente si no se proporciona)
        """
        self._id = session_id or str(uuid.uuid4())
        self._configuration = configuration
        self._board = Board()
        self._players: Dict[PlayerSymbol, Optional[Player]] = {
            PlayerSymbol.X: None,
            PlayerSymbol.O: None
        }
        self._current_player_symbol = PlayerSymbol.X
        self._state = GameState.WAITING_FOR_PLAYERS
        self._result: Optional[GameResult] = None
        self._created_at = datetime.now()
        self._started_at: Optional[datetime] = None
        self._finished_at: Optional[datetime] = None
        self._move_count = 0
    
    @property
    def id(self) -> str:
        """ID único de la sesión."""
        return self._id
    
    @property
    def configuration(self) -> GameConfiguration:
        """Configuración del juego."""
        return self._configuration
    
    @property
    def board(self) -> Board:
        """Tablero del juego."""
        return self._board
    
    @property
    def state(self) -> GameState:
        """Estado actual del juego."""
        return self._state
    
    @property
    def result(self) -> Optional[GameResult]:
        """Resultado del juego (None si no ha terminado)."""
        return self._result
    
    @property
    def current_player(self) -> Optional[Player]:
        """Jugador actual."""
        return self._players[self._current_player_symbol]
    
    @property
    def current_player_symbol(self) -> PlayerSymbol:
        """Símbolo del jugador actual."""
        return self._current_player_symbol
    
    @property
    def players(self) -> List[Player]:
        """Lista de jugadores en el juego."""
        return [player for player in self._players.values() if player is not None]
    
    @property
    def player_x(self) -> Optional[Player]:
        """Jugador X."""
        return self._players[PlayerSymbol.X]
    
    @property
    def player_o(self) -> Optional[Player]:
        """Jugador O."""
        return self._players[PlayerSymbol.O]
    
    @property
    def move_count(self) -> int:
        """Número de movimientos realizados."""
        return self._move_count
    
    @property
    def created_at(self) -> datetime:
        """Fecha y hora de creación de la sesión."""
        return self._created_at
    
    @property
    def started_at(self) -> Optional[datetime]:
        """Fecha y hora de inicio del juego."""
        return self._started_at
    
    @property
    def finished_at(self) -> Optional[datetime]:
        """Fecha y hora de finalización del juego."""
        return self._finished_at
    
    @property
    def duration(self) -> Optional[float]:
        """Duración del juego en segundos."""
        if self._started_at is None:
            return None
        
        end_time = self._finished_at or datetime.now()
        return (end_time - self._started_at).total_seconds()
    
    def add_player(self, player: Player, symbol: PlayerSymbol) -> bool:
        """
        Añade un jugador al juego.
        
        Args:
            player: Jugador a añadir
            symbol: Símbolo asignado al jugador
            
        Returns:
            True si el jugador fue añadido exitosamente, False en caso contrario
            
        Raises:
            ValueError: Si el juego ya está en progreso o el símbolo ya está ocupado
        """
        if self._state != GameState.WAITING_FOR_PLAYERS:
            raise ValueError("No se pueden añadir jugadores una vez iniciado el juego")
        
        if self._players[symbol] is not None:
            return False
        
        # Asignar símbolo al jugador
        player.assign_symbol(symbol)
        self._players[symbol] = player
        
        # Si tenemos dos jugadores, podemos iniciar
        if all(player is not None for player in self._players.values()):
            self._state = GameState.IN_PROGRESS
            self._started_at = datetime.now()
        
        return True
    
    def make_move(self, position: Position, player: Player) -> bool:
        """
        Realiza un movimiento en el juego.
        
        Args:
            position: Posición donde realizar el movimiento
            player: Jugador que realiza el movimiento
            
        Returns:
            True si el movimiento fue exitoso, False en caso contrario
            
        Raises:
            ValueError: Si no es el turno del jugador o el juego no está en progreso
        """
        if self._state != GameState.IN_PROGRESS:
            raise ValueError("El juego no está en progreso")
        
        if player != self.current_player:
            raise ValueError("No es el turno de este jugador")
        
        if player.symbol is None:
            raise ValueError("El jugador no tiene símbolo asignado")
        
        # Convertir PlayerSymbol a CellState
        cell_state = CellState.PLAYER_X if player.symbol == PlayerSymbol.X else CellState.PLAYER_O
        
        # Crear y realizar el movimiento
        move = Move(position=position, player=cell_state)
        
        if not self._board.place_move(move):
            return False
        
        self._move_count += 1
        
        # Verificar si el juego ha terminado
        self._check_game_end()
        
        # Cambiar turno si el juego continúa
        if self._state == GameState.IN_PROGRESS:
            self._switch_turn()
        
        return True
    
    def _check_game_end(self) -> None:
        """Verifica si el juego ha terminado y actualiza el estado."""
        winner = self._board.get_winner()
        
        if winner == CellState.PLAYER_X:
            self._end_game(GameResult.PLAYER_X_WINS)
        elif winner == CellState.PLAYER_O:
            self._end_game(GameResult.PLAYER_O_WINS)
        elif self._board.is_full():
            self._end_game(GameResult.DRAW)
    
    def _end_game(self, result: GameResult) -> None:
        """
        Termina el juego con el resultado especificado.
        
        Args:
            result: Resultado del juego
        """
        self._state = GameState.FINISHED
        self._result = result
        self._finished_at = datetime.now()
        
        # Actualizar estadísticas de los jugadores
        if self._configuration.enable_statistics:
            self._update_player_statistics()
    
    def _update_player_statistics(self) -> None:
        """Actualiza las estadísticas de los jugadores basado en el resultado."""
        if self._result == GameResult.PLAYER_X_WINS:
            if self.player_x:
                self.player_x.record_game_won()
            if self.player_o:
                self.player_o.record_game_lost()
        elif self._result == GameResult.PLAYER_O_WINS:
            if self.player_o:
                self.player_o.record_game_won()
            if self.player_x:
                self.player_x.record_game_lost()
        elif self._result == GameResult.DRAW:
            if self.player_x:
                self.player_x.record_game_drawn()
            if self.player_o:
                self.player_o.record_game_drawn()
    
    def _switch_turn(self) -> None:
        """Cambia el turno al siguiente jugador."""
        self._current_player_symbol = (
            PlayerSymbol.O if self._current_player_symbol == PlayerSymbol.X 
            else PlayerSymbol.X
        )
    
    def pause(self) -> None:
        """Pausa el juego."""
        if self._state == GameState.IN_PROGRESS:
            self._state = GameState.PAUSED
    
    def resume(self) -> None:
        """Reanuda el juego."""
        if self._state == GameState.PAUSED:
            self._state = GameState.IN_PROGRESS
    
    def abandon(self) -> None:
        """Abandona el juego."""
        if self._state in [GameState.IN_PROGRESS, GameState.PAUSED]:
            self._end_game(GameResult.ABANDONED)
    
    def reset(self) -> None:
        """Reinicia el juego para una nueva partida."""
        self._board.reset()
        self._current_player_symbol = PlayerSymbol.X
        self._state = GameState.IN_PROGRESS if len(self.players) == 2 else GameState.WAITING_FOR_PLAYERS
        self._result = None
        self._started_at = datetime.now() if len(self.players) == 2 else None
        self._finished_at = None
        self._move_count = 0
    
    def get_winner(self) -> Optional[Player]:
        """
        Obtiene el jugador ganador.
        
        Returns:
            Jugador ganador o None si no hay ganador o el juego no ha terminado
        """
        if self._result == GameResult.PLAYER_X_WINS:
            return self.player_x
        elif self._result == GameResult.PLAYER_O_WINS:
            return self.player_o
        return None
    
    def is_draw(self) -> bool:
        """Verifica si el juego terminó en empate."""
        return self._result == GameResult.DRAW
    
    def is_finished(self) -> bool:
        """Verifica si el juego ha terminado."""
        return self._state == GameState.FINISHED
    
    def get_available_moves(self) -> List[Position]:
        """Obtiene las posiciones disponibles para mover."""
        return self._board.get_empty_positions()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la sesión a diccionario para serialización."""
        return {
            'id': self._id,
            'state': self._state.value,
            'result': self._result.value if self._result else None,
            'current_player_symbol': self._current_player_symbol.value,
            'move_count': self._move_count,
            'created_at': self._created_at.isoformat(),
            'started_at': self._started_at.isoformat() if self._started_at else None,
            'finished_at': self._finished_at.isoformat() if self._finished_at else None,
            'board': self._board.to_list(),
            'players': {
                symbol.value: player.to_dict() if hasattr(player, 'to_dict') else str(player)
                for symbol, player in self._players.items() 
                if player is not None
            }
        }
    
    def __str__(self) -> str:
        """Representación string de la sesión."""
        return f"GameSession {self._id} - Estado: {self._state.value}, Movimientos: {self._move_count}"
    
    def __repr__(self) -> str:
        """Representación detallada de la sesión para debug."""
        return (
            f"GameSession(id='{self._id}', state={self._state.value}, "
            f"result={self._result.value if self._result else None}, "
            f"players={len(self.players)}, moves={self._move_count})"
        )