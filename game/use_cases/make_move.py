"""
Caso de Uso: Realizar Movimiento en Tres en Raya.

Este caso de uso encapsula toda la lógica necesaria para realizar
un movimiento en el juego, incluyendo validaciones, actualización
del estado y verificación de condiciones de victoria.
"""

from typing import List, Optional
from dataclasses import dataclass

from game.entities import (
    GameSession, Position, Player, GameState, GameResult
)


@dataclass
class MakeMoveRequest:
    """Petición para realizar un movimiento."""
    game_session_id: str
    player_id: str
    row: int
    col: int


@dataclass
class MakeMoveResponse:
    """Respuesta del caso de uso realizar movimiento."""
    success: bool
    message: str
    game_session: Optional[GameSession]
    is_game_over: bool
    winner: Optional[Player]
    is_draw: bool
    errors: List[str]


class MakeMoveUseCase:
    """
    Caso de uso para realizar un movimiento en Tres en Raya.
    
    Este caso de uso implementa la lógica de negocio para:
    - Validar que el movimiento es válido
    - Verificar que es el turno del jugador correcto
    - Actualizar el estado del tablero
    - Verificar condiciones de victoria o empate
    - Cambiar el turno al siguiente jugador
    
    Principios de Screaming Architecture aplicados:
    - Se enfoca en el DOMINIO: Realizar movimiento en Tres en Raya
    - Encapsula las reglas de negocio para los movimientos
    - No depende de frameworks o tecnologías específicas
    - Utiliza entidades del dominio
    """
    
    def __init__(self, game_session_repository):
        """
        Inicializa el caso de uso.
        
        Args:
            game_session_repository: Repositorio para obtener/guardar sesiones de juego
        """
        self._game_session_repository = game_session_repository
    
    def execute(self, request: MakeMoveRequest) -> MakeMoveResponse:
        """
        Ejecuta el caso de uso de realizar movimiento.
        
        Args:
            request: Datos necesarios para realizar el movimiento
            
        Returns:
            Respuesta con el resultado de la operación
        """
        # Validar datos de entrada
        errors = self._validate_request(request)
        if errors:
            return MakeMoveResponse(
                success=False,
                message="Error de validación en el movimiento",
                game_session=None,
                is_game_over=False,
                winner=None,
                is_draw=False,
                errors=errors
            )
        
        try:
            # Obtener la sesión de juego
            game_session = self._game_session_repository.get_by_id(request.game_session_id)
            if not game_session:
                return MakeMoveResponse(
                    success=False,
                    message="Sesión de juego no encontrada",
                    game_session=None,
                    is_game_over=False,
                    winner=None,
                    is_draw=False,
                    errors=["Sesión de juego no encontrada"]
                )
            
            # Validar el estado del juego
            validation_errors = self._validate_game_state(game_session, request.player_id)
            if validation_errors:
                return MakeMoveResponse(
                    success=False,
                    message="Estado del juego inválido para realizar movimiento",
                    game_session=game_session,
                    is_game_over=False,
                    winner=None,
                    is_draw=False,
                    errors=validation_errors
                )
            
            # Buscar el jugador
            player = self._find_player_by_id(game_session, request.player_id)
            if not player:
                return MakeMoveResponse(
                    success=False,
                    message="Jugador no encontrado en la sesión",
                    game_session=game_session,
                    is_game_over=False,
                    winner=None,
                    is_draw=False,
                    errors=["Jugador no encontrado en la sesión"]
                )
            
            # Crear la posición del movimiento
            position = Position(row=request.row, col=request.col)
            
            # Realizar el movimiento
            move_success = game_session.make_move(position, player)
            
            if not move_success:
                return MakeMoveResponse(
                    success=False,
                    message="No se pudo realizar el movimiento - posición ocupada",
                    game_session=game_session,
                    is_game_over=False,
                    winner=None,
                    is_draw=False,
                    errors=["La posición seleccionada ya está ocupada"]
                )
            
            # Guardar la sesión actualizada
            self._game_session_repository.save(game_session)
            
            # Preparar respuesta exitosa
            return MakeMoveResponse(
                success=True,
                message=self._build_success_message(game_session, player),
                game_session=game_session,
                is_game_over=game_session.is_finished(),
                winner=game_session.get_winner(),
                is_draw=game_session.is_draw(),
                errors=[]
            )
            
        except ValueError as e:
            return MakeMoveResponse(
                success=False,
                message="Error de validación",
                game_session=None,
                is_game_over=False,
                winner=None,
                is_draw=False,
                errors=[str(e)]
            )
        except Exception as e:
            return MakeMoveResponse(
                success=False,
                message="Error interno al realizar el movimiento",
                game_session=None,
                is_game_over=False,
                winner=None,
                is_draw=False,
                errors=[f"Error interno: {str(e)}"]
            )
    
    def _validate_request(self, request: MakeMoveRequest) -> List[str]:
        """
        Valida los datos de la petición.
        
        Args:
            request: Petición a validar
            
        Returns:
            Lista de errores de validación (vacía si es válida)
        """
        errors = []
        
        # Validar ID de sesión
        if not request.game_session_id or not request.game_session_id.strip():
            errors.append("ID de sesión de juego es obligatorio")
        
        # Validar ID de jugador
        if not request.player_id or not request.player_id.strip():
            errors.append("ID de jugador es obligatorio")
        
        # Validar coordenadas
        if not (0 <= request.row <= 2):
            errors.append("La fila debe estar entre 0 y 2")
        
        if not (0 <= request.col <= 2):
            errors.append("La columna debe estar entre 0 y 2")
        
        return errors
    
    def _validate_game_state(self, game_session: GameSession, player_id: str) -> List[str]:
        """
        Valida que el estado del juego permita realizar movimientos.
        
        Args:
            game_session: Sesión de juego a validar
            player_id: ID del jugador que intenta mover
            
        Returns:
            Lista de errores de validación (vacía si es válida)
        """
        errors = []
        
        # Verificar que el juego esté en progreso
        if game_session.state != GameState.IN_PROGRESS:
            errors.append(f"El juego no está en progreso. Estado actual: {game_session.state.value}")
        
        # Verificar que sea el turno del jugador correcto
        current_player = game_session.current_player
        if not current_player or current_player.id != player_id:
            current_name = current_player.name if current_player else "Desconocido"
            errors.append(f"No es el turno de este jugador. Turno actual: {current_name}")
        
        return errors
    
    def _find_player_by_id(self, game_session: GameSession, player_id: str) -> Optional[Player]:
        """
        Busca un jugador por su ID en la sesión de juego.
        
        Args:
            game_session: Sesión de juego donde buscar
            player_id: ID del jugador a buscar
            
        Returns:
            Jugador encontrado o None si no existe
        """
        for player in game_session.players:
            if player.id == player_id:
                return player
        return None
    
    def _build_success_message(self, game_session: GameSession, player: Player) -> str:
        """
        Construye el mensaje de éxito basado en el resultado del movimiento.
        
        Args:
            game_session: Sesión de juego actualizada
            player: Jugador que realizó el movimiento
            
        Returns:
            Mensaje de éxito apropiado
        """
        if game_session.is_finished():
            if game_session.is_draw():
                return "¡Empate! El tablero está completo y no hay ganador"
            else:
                winner = game_session.get_winner()
                winner_name = winner.name if winner else "Desconocido"
                return f"¡{winner_name} ha ganado la partida!"
        else:
            next_player = game_session.current_player
            next_name = next_player.name if next_player else "Desconocido"
            return f"Movimiento realizado por {player.name}. Turno de {next_name}"


class MakeMoveUseCaseFactory:
    """Factory para crear instancias del caso de uso MakeMove."""
    
    @staticmethod
    def create(game_session_repository) -> MakeMoveUseCase:
        """
        Crea una nueva instancia del caso de uso.
        
        Args:
            game_session_repository: Repositorio de sesiones de juego
            
        Returns:
            Nueva instancia de MakeMoveUseCase
        """
        return MakeMoveUseCase(game_session_repository)