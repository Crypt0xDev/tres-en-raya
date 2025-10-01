"""
Caso de Uso: Verificar Ganador en Tres en Raya.

Este caso de uso encapsula toda la lógica necesaria para verificar
si hay un ganador en el juego y determinar el resultado de la partida.
"""

from typing import Optional, List
from dataclasses import dataclass

from game.entities import GameSession, GameResult, GameState, Player


@dataclass
class CheckWinnerRequest:
    """Petición para verificar ganador."""
    game_session_id: str


@dataclass
class CheckWinnerResponse:
    """Respuesta del caso de uso verificar ganador."""
    success: bool
    message: str
    has_winner: bool
    winner: Optional[Player]
    is_draw: bool
    is_game_over: bool
    game_session: Optional[GameSession]
    errors: List[str]


class CheckWinnerUseCase:
    """
    Caso de uso para verificar ganador en Tres en Raya.
    
    Este caso de uso implementa la lógica de negocio para:
    - Verificar si hay un ganador en el tablero actual
    - Determinar si el juego ha terminado en empate
    - Actualizar el estado del juego según el resultado
    - Proporcionar información detallada del resultado
    
    Principios de Screaming Architecture aplicados:
    - Se enfoca en el DOMINIO: Verificar ganador en Tres en Raya
    - Encapsula las reglas de negocio para determinar resultados
    - No depende de frameworks o tecnologías específicas
    - Utiliza entidades del dominio
    """
    
    def __init__(self, game_session_repository):
        """
        Inicializa el caso de uso.
        
        Args:
            game_session_repository: Repositorio para obtener sesiones de juego
        """
        self._game_session_repository = game_session_repository
    
    def execute(self, request: CheckWinnerRequest) -> CheckWinnerResponse:
        """
        Ejecuta el caso de uso de verificar ganador.
        
        Args:
            request: Datos necesarios para verificar el ganador
            
        Returns:
            Respuesta con el resultado de la verificación
        """
        # Validar datos de entrada
        errors = self._validate_request(request)
        if errors:
            return CheckWinnerResponse(
                success=False,
                message="Error de validación",
                has_winner=False,
                winner=None,
                is_draw=False,
                is_game_over=False,
                game_session=None,
                errors=errors
            )
        
        try:
            # Obtener la sesión de juego
            game_session = self._game_session_repository.get_by_id(request.game_session_id)
            if not game_session:
                return CheckWinnerResponse(
                    success=False,
                    message="Sesión de juego no encontrada",
                    has_winner=False,
                    winner=None,
                    is_draw=False,
                    is_game_over=False,
                    game_session=None,
                    errors=["Sesión de juego no encontrada"]
                )
            
            # Verificar estado del juego
            validation_errors = self._validate_game_state(game_session)
            if validation_errors:
                return CheckWinnerResponse(
                    success=False,
                    message="Estado del juego inválido",
                    has_winner=False,
                    winner=None,
                    is_draw=False,
                    is_game_over=False,
                    game_session=game_session,
                    errors=validation_errors
                )
            
            # Verificar ganador
            winner = game_session.get_winner()
            is_draw = game_session.is_draw()
            is_game_over = game_session.is_finished()
            
            # Construir mensaje de resultado
            message = self._build_result_message(winner, is_draw, is_game_over)
            
            return CheckWinnerResponse(
                success=True,
                message=message,
                has_winner=winner is not None,
                winner=winner,
                is_draw=is_draw,
                is_game_over=is_game_over,
                game_session=game_session,
                errors=[]
            )
            
        except Exception as e:
            return CheckWinnerResponse(
                success=False,
                message="Error interno al verificar ganador",
                has_winner=False,
                winner=None,
                is_draw=False,
                is_game_over=False,
                game_session=None,
                errors=[f"Error interno: {str(e)}"]
            )
    
    def _validate_request(self, request: CheckWinnerRequest) -> List[str]:
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
        
        return errors
    
    def _validate_game_state(self, game_session: GameSession) -> List[str]:
        """
        Valida que el estado del juego sea válido para verificación.
        
        Args:
            game_session: Sesión de juego a validar
            
        Returns:
            Lista de errores de validación (vacía si es válida)
        """
        errors = []
        
        # Verificar que el juego tenga jugadores
        if len(game_session.players) < 2:
            errors.append("El juego debe tener al menos 2 jugadores")
        
        # Verificar que el juego haya comenzado
        if game_session.state == GameState.WAITING_FOR_PLAYERS:
            errors.append("El juego aún no ha comenzado")
        
        return errors
    
    def _build_result_message(
        self, 
        winner: Optional[Player], 
        is_draw: bool, 
        is_game_over: bool
    ) -> str:
        """
        Construye el mensaje de resultado basado en el estado del juego.
        
        Args:
            winner: Jugador ganador (si existe)
            is_draw: Si el juego terminó en empate
            is_game_over: Si el juego ha terminado
            
        Returns:
            Mensaje descriptivo del resultado
        """
        if winner:
            return f"¡{winner.name} ha ganado la partida!"
        elif is_draw:
            return "La partida ha terminado en empate"
        elif is_game_over:
            return "La partida ha terminado sin resultado"
        else:
            return "El juego está en progreso, aún no hay ganador"


class CheckWinnerUseCaseFactory:
    """Factory para crear instancias del caso de uso CheckWinner."""
    
    @staticmethod
    def create(game_session_repository) -> CheckWinnerUseCase:
        """
        Crea una nueva instancia del caso de uso.
        
        Args:
            game_session_repository: Repositorio de sesiones de juego
            
        Returns:
            Nueva instancia de CheckWinnerUseCase
        """
        return CheckWinnerUseCase(game_session_repository)