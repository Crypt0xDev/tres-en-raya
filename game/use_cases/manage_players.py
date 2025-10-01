"""
Caso de Uso: Gestionar Jugadores en Tres en Raya.

Este caso de uso encapsula toda la lógica necesaria para gestionar
jugadores, incluyendo creación, configuración y estadísticas.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from game.entities import Player, PlayerType, PlayerSymbol, PlayerStats


@dataclass
class CreatePlayerRequest:
    """Petición para crear un jugador."""
    name: str
    player_type: PlayerType = PlayerType.HUMAN
    player_id: Optional[str] = None


@dataclass
class UpdatePlayerStatsRequest:
    """Petición para actualizar estadísticas de jugador."""
    player_id: str
    games_won: int = 0
    games_lost: int = 0
    games_drawn: int = 0


@dataclass
class GetPlayerStatsRequest:
    """Petición para obtener estadísticas de jugador."""
    player_id: str


@dataclass
class ManagePlayersResponse:
    """Respuesta del caso de uso gestionar jugadores."""
    success: bool
    message: str
    player: Optional[Player]
    players: List[Player]
    stats: Optional[Dict[str, Any]]
    errors: List[str]


class ManagePlayersUseCase:
    """
    Caso de uso para gestionar jugadores en Tres en Raya.
    
    Este caso de uso implementa la lógica de negocio para:
    - Crear nuevos jugadores con validaciones
    - Actualizar estadísticas de jugadores
    - Obtener información de jugadores
    - Gestionar tipos de jugadores (humanos, IA)
    
    Principios de Screaming Architecture aplicados:
    - Se enfoca en el DOMINIO: Gestión de jugadores de Tres en Raya
    - Encapsula las reglas de negocio para jugadores
    - No depende de frameworks o tecnologías específicas
    - Utiliza entidades del dominio
    """
    
    def __init__(self, player_repository):
        """
        Inicializa el caso de uso.
        
        Args:
            player_repository: Repositorio para gestionar jugadores
        """
        self._player_repository = player_repository
    
    def create_player(self, request: CreatePlayerRequest) -> ManagePlayersResponse:
        """
        Crea un nuevo jugador.
        
        Args:
            request: Datos para crear el jugador
            
        Returns:
            Respuesta con el resultado de la operación
        """
        # Validar datos de entrada
        errors = self._validate_create_request(request)
        if errors:
            return ManagePlayersResponse(
                success=False,
                message="Error de validación al crear jugador",
                player=None,
                players=[],
                stats=None,
                errors=errors
            )
        
        try:
            # Verificar si ya existe un jugador con el mismo nombre
            if self._player_repository.exists_by_name(request.name):
                return ManagePlayersResponse(
                    success=False,
                    message="Ya existe un jugador con ese nombre",
                    player=None,
                    players=[],
                    stats=None,
                    errors=["Nombre de jugador duplicado"]
                )
            
            # Crear jugador
            player = Player(
                name=request.name,
                player_type=request.player_type,
                player_id=request.player_id
            )
            
            # Guardar jugador
            saved = self._player_repository.save(player)
            if not saved:
                return ManagePlayersResponse(
                    success=False,
                    message="No se pudo guardar el jugador",
                    player=None,
                    players=[],
                    stats=None,
                    errors=["Error al guardar en repositorio"]
                )
            
            return ManagePlayersResponse(
                success=True,
                message=f"Jugador '{player.name}' creado exitosamente",
                player=player,
                players=[],
                stats=None,
                errors=[]
            )
            
        except Exception as e:
            return ManagePlayersResponse(
                success=False,
                message="Error interno al crear jugador",
                player=None,
                players=[],
                stats=None,
                errors=[f"Error interno: {str(e)}"]
            )
    
    def update_player_stats(self, request: UpdatePlayerStatsRequest) -> ManagePlayersResponse:
        """
        Actualiza las estadísticas de un jugador.
        
        Args:
            request: Datos para actualizar estadísticas
            
        Returns:
            Respuesta con el resultado de la operación
        """
        # Validar datos de entrada
        errors = self._validate_stats_request(request)
        if errors:
            return ManagePlayersResponse(
                success=False,
                message="Error de validación al actualizar estadísticas",
                player=None,
                players=[],
                stats=None,
                errors=errors
            )
        
        try:
            # Obtener jugador
            player = self._player_repository.get_by_id(request.player_id)
            if not player:
                return ManagePlayersResponse(
                    success=False,
                    message="Jugador no encontrado",
                    player=None,
                    players=[],
                    stats=None,
                    errors=["Jugador no existe"]
                )
            
            # Actualizar estadísticas
            for _ in range(request.games_won):
                player.record_game_won()
            
            for _ in range(request.games_lost):
                player.record_game_lost()
            
            for _ in range(request.games_drawn):
                player.record_game_drawn()
            
            # Guardar cambios
            saved = self._player_repository.save(player)
            if not saved:
                return ManagePlayersResponse(
                    success=False,
                    message="No se pudieron guardar las estadísticas",
                    player=None,
                    players=[],
                    stats=None,
                    errors=["Error al guardar cambios"]
                )
            
            return ManagePlayersResponse(
                success=True,
                message=f"Estadísticas de '{player.name}' actualizadas",
                player=player,
                players=[],
                stats=self._serialize_player_stats(player.stats),
                errors=[]
            )
            
        except Exception as e:
            return ManagePlayersResponse(
                success=False,
                message="Error interno al actualizar estadísticas",
                player=None,
                players=[],
                stats=None,
                errors=[f"Error interno: {str(e)}"]
            )
    
    def get_player_stats(self, request: GetPlayerStatsRequest) -> ManagePlayersResponse:
        """
        Obtiene las estadísticas de un jugador.
        
        Args:
            request: Datos para obtener estadísticas
            
        Returns:
            Respuesta con las estadísticas del jugador
        """
        try:
            # Obtener jugador
            player = self._player_repository.get_by_id(request.player_id)
            if not player:
                return ManagePlayersResponse(
                    success=False,
                    message="Jugador no encontrado",
                    player=None,
                    players=[],
                    stats=None,
                    errors=["Jugador no existe"]
                )
            
            return ManagePlayersResponse(
                success=True,
                message=f"Estadísticas de '{player.name}' obtenidas",
                player=player,
                players=[],
                stats=self._serialize_player_stats(player.stats),
                errors=[]
            )
            
        except Exception as e:
            return ManagePlayersResponse(
                success=False,
                message="Error interno al obtener estadísticas",
                player=None,
                players=[],
                stats=None,
                errors=[f"Error interno: {str(e)}"]
            )
    
    def get_all_players(self) -> ManagePlayersResponse:
        """
        Obtiene todos los jugadores del sistema.
        
        Returns:
            Respuesta con la lista de jugadores
        """
        try:
            players = self._player_repository.get_all()
            
            return ManagePlayersResponse(
                success=True,
                message=f"Se encontraron {len(players)} jugadores",
                player=None,
                players=players,
                stats=None,
                errors=[]
            )
            
        except Exception as e:
            return ManagePlayersResponse(
                success=False,
                message="Error interno al obtener jugadores",
                player=None,
                players=[],
                stats=None,
                errors=[f"Error interno: {str(e)}"]
            )
    
    def get_top_players(self, limit: int = 10) -> ManagePlayersResponse:
        """
        Obtiene el ranking de mejores jugadores.
        
        Args:
            limit: Número máximo de jugadores a retornar
            
        Returns:
            Respuesta con el ranking de jugadores
        """
        try:
            all_players = self._player_repository.get_all()
            
            # Ordenar por tasa de victoria y número de partidas jugadas
            top_players = sorted(
                [p for p in all_players if p.stats.games_played > 0],
                key=lambda p: (p.stats.win_rate, p.stats.games_played),
                reverse=True
            )[:limit]
            
            return ManagePlayersResponse(
                success=True,
                message=f"Top {len(top_players)} jugadores obtenidos",
                player=None,
                players=top_players,
                stats=None,
                errors=[]
            )
            
        except Exception as e:
            return ManagePlayersResponse(
                success=False,
                message="Error interno al obtener ranking",
                player=None,
                players=[],
                stats=None,
                errors=[f"Error interno: {str(e)}"]
            )
    
    def _validate_create_request(self, request: CreatePlayerRequest) -> List[str]:
        """
        Valida los datos para crear un jugador.
        
        Args:
            request: Petición a validar
            
        Returns:
            Lista de errores de validación (vacía si es válida)
        """
        errors = []
        
        # Validar nombre
        if not request.name or not request.name.strip():
            errors.append("El nombre del jugador es obligatorio")
        elif len(request.name.strip()) < 2:
            errors.append("El nombre debe tener al menos 2 caracteres")
        elif len(request.name.strip()) > 50:
            errors.append("El nombre no puede exceder 50 caracteres")
        
        # Validar tipo de jugador
        if not isinstance(request.player_type, PlayerType):
            errors.append("Tipo de jugador inválido")
        
        return errors
    
    def _validate_stats_request(self, request: UpdatePlayerStatsRequest) -> List[str]:
        """
        Valida los datos para actualizar estadísticas.
        
        Args:
            request: Petición a validar
            
        Returns:
            Lista de errores de validación (vacía si es válida)
        """
        errors = []
        
        # Validar ID de jugador
        if not request.player_id or not request.player_id.strip():
            errors.append("ID de jugador es obligatorio")
        
        # Validar valores numéricos
        if request.games_won < 0:
            errors.append("Las partidas ganadas no pueden ser negativas")
        
        if request.games_lost < 0:
            errors.append("Las partidas perdidas no pueden ser negativas")
        
        if request.games_drawn < 0:
            errors.append("Las partidas empatadas no pueden ser negativas")
        
        return errors
    
    def _serialize_player_stats(self, stats: PlayerStats) -> Dict[str, Any]:
        """
        Serializa las estadísticas de un jugador.
        
        Args:
            stats: Estadísticas a serializar
            
        Returns:
            Diccionario con las estadísticas
        """
        return {
            'games_played': stats.games_played,
            'games_won': stats.games_won,
            'games_lost': stats.games_lost,
            'games_drawn': stats.games_drawn,
            'win_rate': round(stats.win_rate, 2),
            'loss_rate': round(stats.loss_rate, 2),
            'draw_rate': round(stats.draw_rate, 2)
        }


class ManagePlayersUseCaseFactory:
    """Factory para crear instancias del caso de uso ManagePlayers."""
    
    @staticmethod
    def create(player_repository) -> ManagePlayersUseCase:
        """
        Crea una nueva instancia del caso de uso.
        
        Args:
            player_repository: Repositorio de jugadores
            
        Returns:
            Nueva instancia de ManagePlayersUseCase
        """
        return ManagePlayersUseCase(player_repository)