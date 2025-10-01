"""
Entidad Player - Jugador de Tres en Raya.

Esta entidad representa el concepto de jugador en el dominio del juego.
Encapsula toda la lógica relacionada con la identidad, estadísticas y
comportamiento del jugador.
"""

from typing import Optional
from dataclasses import dataclass
from enum import Enum
import uuid
from datetime import datetime


class PlayerType(Enum):
    """Tipos de jugador en el sistema."""
    HUMAN = "human"
    AI_EASY = "ai_easy"
    AI_MEDIUM = "ai_medium" 
    AI_HARD = "ai_hard"


class PlayerSymbol(Enum):
    """Símbolos válidos para los jugadores."""
    X = "X"
    O = "O"


@dataclass(frozen=True)
class PlayerStats:
    """Estadísticas inmutables de un jugador."""
    games_played: int = 0
    games_won: int = 0
    games_lost: int = 0
    games_drawn: int = 0
    
    @property
    def win_rate(self) -> float:
        """Calcula el porcentaje de victorias."""
        if self.games_played == 0:
            return 0.0
        return (self.games_won / self.games_played) * 100
    
    @property
    def loss_rate(self) -> float:
        """Calcula el porcentaje de derrotas."""
        if self.games_played == 0:
            return 0.0
        return (self.games_lost / self.games_played) * 100
    
    @property
    def draw_rate(self) -> float:
        """Calcula el porcentaje de empates."""
        if self.games_played == 0:
            return 0.0
        return (self.games_drawn / self.games_played) * 100


class Player:
    """
    Entidad Player - Representa un jugador en el juego Tres en Raya.
    
    Esta entidad encapsula toda la lógica del dominio relacionada con
    los jugadores, incluyendo su identidad, tipo, estadísticas y comportamiento.
    
    Principios de Screaming Architecture aplicados:
    - Se enfoca en el DOMINIO: Jugador de Tres en Raya
    - Encapsula reglas de negocio del jugador
    - Utiliza Value Objects para estadísticas y símbolos
    - No depende de tecnologías específicas
    """
    
    def __init__(
        self, 
        name: str, 
        player_type: PlayerType = PlayerType.HUMAN,
        player_id: Optional[str] = None
    ):
        """
        Inicializa un nuevo jugador.
        
        Args:
            name: Nombre del jugador
            player_type: Tipo de jugador (humano o IA)
            player_id: ID único del jugador (se genera automáticamente si no se proporciona)
        
        Raises:
            ValueError: Si el nombre está vacío
        """
        if not name or not name.strip():
            raise ValueError("El nombre del jugador no puede estar vacío")
        
        self._id = player_id or str(uuid.uuid4())
        self._name = name.strip()
        self._player_type = player_type
        self._symbol: Optional[PlayerSymbol] = None
        self._stats = PlayerStats()
        self._created_at = datetime.now()
        self._is_active = True
    
    @property
    def id(self) -> str:
        """ID único del jugador."""
        return self._id
    
    @property
    def name(self) -> str:
        """Nombre del jugador."""
        return self._name
    
    @property
    def player_type(self) -> PlayerType:
        """Tipo de jugador."""
        return self._player_type
    
    @property
    def symbol(self) -> Optional[PlayerSymbol]:
        """Símbolo asignado al jugador."""
        return self._symbol
    
    @property
    def stats(self) -> PlayerStats:
        """Estadísticas del jugador."""
        return self._stats
    
    @property
    def created_at(self) -> datetime:
        """Fecha y hora de creación del jugador."""
        return self._created_at
    
    @property
    def is_active(self) -> bool:
        """Indica si el jugador está activo."""
        return self._is_active
    
    @property
    def is_human(self) -> bool:
        """Verifica si el jugador es humano."""
        return self._player_type == PlayerType.HUMAN
    
    @property
    def is_ai(self) -> bool:
        """Verifica si el jugador es IA."""
        return self._player_type in [
            PlayerType.AI_EASY, 
            PlayerType.AI_MEDIUM, 
            PlayerType.AI_HARD
        ]
    
    def assign_symbol(self, symbol: PlayerSymbol) -> None:
        """
        Asigna un símbolo al jugador.
        
        Args:
            symbol: Símbolo a asignar (X o O)
            
        Raises:
            ValueError: Si se intenta cambiar un símbolo ya asignado
        """
        if self._symbol is not None:
            raise ValueError(f"El jugador {self._name} ya tiene asignado el símbolo {self._symbol.value}")
        
        self._symbol = symbol
    
    def change_name(self, new_name: str) -> None:
        """
        Cambia el nombre del jugador.
        
        Args:
            new_name: Nuevo nombre del jugador
            
        Raises:
            ValueError: Si el nuevo nombre está vacío
        """
        if not new_name or not new_name.strip():
            raise ValueError("El nuevo nombre no puede estar vacío")
        
        self._name = new_name.strip()
    
    def record_game_won(self) -> None:
        """Registra una victoria del jugador."""
        self._stats = PlayerStats(
            games_played=self._stats.games_played + 1,
            games_won=self._stats.games_won + 1,
            games_lost=self._stats.games_lost,
            games_drawn=self._stats.games_drawn
        )
    
    def record_game_lost(self) -> None:
        """Registra una derrota del jugador."""
        self._stats = PlayerStats(
            games_played=self._stats.games_played + 1,
            games_won=self._stats.games_won,
            games_lost=self._stats.games_lost + 1,
            games_drawn=self._stats.games_drawn
        )
    
    def record_game_drawn(self) -> None:
        """Registra un empate del jugador."""
        self._stats = PlayerStats(
            games_played=self._stats.games_played + 1,
            games_won=self._stats.games_won,
            games_lost=self._stats.games_lost,
            games_drawn=self._stats.games_drawn + 1
        )
    
    def deactivate(self) -> None:
        """Desactiva al jugador."""
        self._is_active = False
    
    def activate(self) -> None:
        """Activa al jugador."""
        self._is_active = True
    
    def reset_stats(self) -> None:
        """Reinicia las estadísticas del jugador."""
        self._stats = PlayerStats()
    
    def __eq__(self, other) -> bool:
        """Compara jugadores por su ID único."""
        if not isinstance(other, Player):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        """Hash basado en el ID del jugador."""
        return hash(self._id)
    
    def __str__(self) -> str:
        """Representación string del jugador."""
        symbol_str = self._symbol.value if self._symbol else "Sin símbolo"
        return f"Jugador {self._name} ({symbol_str}) - Tipo: {self._player_type.value}"
    
    def to_dict(self) -> dict:
        """Convierte el jugador a diccionario para serialización."""
        return {
            'id': self._id,
            'name': self._name,
            'player_type': self._player_type.value,
            'symbol': self._symbol.value if self._symbol else None,
            'stats': {
                'games_played': self._stats.games_played,
                'games_won': self._stats.games_won,
                'games_lost': self._stats.games_lost,
                'games_drawn': self._stats.games_drawn,
                'win_rate': self._stats.win_rate,
                'loss_rate': self._stats.loss_rate,
                'draw_rate': self._stats.draw_rate
            },
            'created_at': self._created_at.isoformat(),
            'is_active': self._is_active
        }
    
    def __repr__(self) -> str:
        """Representación detallada del jugador para debug."""
        return (
            f"Player(id='{self._id}', name='{self._name}', "
            f"type={self._player_type.value}, symbol={self._symbol}, "
            f"stats={self._stats})"
        )