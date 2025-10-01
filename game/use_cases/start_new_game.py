"""
Caso de Uso: Iniciar Nueva Partida de Tres en Raya.

Este caso de uso encapsula toda la lógica necesaria para iniciar
una nueva partida del juego, incluyendo la configuración inicial,
validaciones y preparación del estado del juego.
"""

from typing import Optional, List
from dataclasses import dataclass

from game.entities import (
    GameSession, GameConfiguration, Player, PlayerSymbol, PlayerType
)


@dataclass
class StartNewGameRequest:
    """Petición para iniciar una nueva partida."""
    player1_name: str
    player2_name: Optional[str] = None
    player2_type: PlayerType = PlayerType.HUMAN
    configuration: Optional[GameConfiguration] = None
    session_id: Optional[str] = None


@dataclass
class StartNewGameResponse:
    """Respuesta del caso de uso iniciar nueva partida."""
    game_session: Optional[GameSession]
    success: bool
    message: str
    errors: List[str]


class StartNewGameUseCase:
    """
    Caso de uso para iniciar una nueva partida de Tres en Raya.
    
    Este caso de uso implementa la lógica de negocio para:
    - Validar los datos de entrada
    - Crear los jugadores necesarios
    - Configurar la sesión de juego
    - Asignar símbolos a los jugadores
    - Preparar el estado inicial del juego
    
    Principios de Screaming Architecture aplicados:
    - Se enfoca en el DOMINIO: Iniciar partida de Tres en Raya
    - Encapsula las reglas de negocio para el inicio de partidas
    - No depende de frameworks o tecnologías específicas
    - Utiliza entidades del dominio
    """
    
    def execute(self, request: StartNewGameRequest) -> StartNewGameResponse:
        """
        Ejecuta el caso de uso de iniciar nueva partida.
        
        Args:
            request: Datos necesarios para iniciar la partida
            
        Returns:
            Respuesta con el resultado de la operación
        """
        errors = self._validate_request(request)
        
        if errors:
            return StartNewGameResponse(
                game_session=None,
                success=False,
                message="Error de validación al iniciar la partida",
                errors=errors
            )
        
        try:
            # Crear configuración del juego
            configuration = request.configuration or GameConfiguration()
            
            # Crear sesión de juego
            game_session = GameSession(
                configuration=configuration,
                session_id=request.session_id
            )
            
            # Crear jugadores
            player1 = Player(
                name=request.player1_name,
                player_type=PlayerType.HUMAN
            )
            
            # Crear segundo jugador (humano o IA)
            if request.player2_name:
                player2 = Player(
                    name=request.player2_name,
                    player_type=request.player2_type
                )
            else:
                # Si no se proporciona nombre, crear jugador IA con nombre por defecto
                ai_names = {
                    PlayerType.AI_EASY: "IA Fácil",
                    PlayerType.AI_MEDIUM: "IA Medio", 
                    PlayerType.AI_HARD: "IA Difícil"
                }
                player2_name = ai_names.get(request.player2_type, "Jugador 2")
                player2 = Player(
                    name=player2_name,
                    player_type=request.player2_type
                )
            
            # Asignar jugadores a la sesión
            # Por convención, el primer jugador siempre es X
            game_session.add_player(player1, PlayerSymbol.X)
            game_session.add_player(player2, PlayerSymbol.O)
            
            return StartNewGameResponse(
                game_session=game_session,
                success=True,
                message=f"Partida iniciada exitosamente entre {player1.name} y {player2.name}",
                errors=[]
            )
            
        except Exception as e:
            return StartNewGameResponse(
                game_session=None,
                success=False,
                message="Error interno al iniciar la partida",
                errors=[str(e)]
            )
    
    def _validate_request(self, request: StartNewGameRequest) -> List[str]:
        """
        Valida los datos de la petición.
        
        Args:
            request: Petición a validar
            
        Returns:
            Lista de errores de validación (vacía si es válida)
        """
        errors = []
        
        # Validar nombre del jugador 1
        if not request.player1_name or not request.player1_name.strip():
            errors.append("El nombre del jugador 1 es obligatorio")
        elif len(request.player1_name.strip()) < 2:
            errors.append("El nombre del jugador 1 debe tener al menos 2 caracteres")
        elif len(request.player1_name.strip()) > 50:
            errors.append("El nombre del jugador 1 no puede exceder 50 caracteres")
        
        # Validar nombre del jugador 2 si se proporciona
        if request.player2_name is not None:
            if not request.player2_name.strip():
                errors.append("Si se proporciona, el nombre del jugador 2 no puede estar vacío")
            elif len(request.player2_name.strip()) < 2:
                errors.append("El nombre del jugador 2 debe tener al menos 2 caracteres")
            elif len(request.player2_name.strip()) > 50:
                errors.append("El nombre del jugador 2 no puede exceder 50 caracteres")
            elif request.player1_name.strip().lower() == request.player2_name.strip().lower():
                errors.append("Los jugadores deben tener nombres diferentes")
        
        # Validar tipo de jugador 2
        if not isinstance(request.player2_type, PlayerType):
            errors.append("Tipo de jugador 2 inválido")
        
        # Validar configuración si se proporciona
        if request.configuration:
            if request.configuration.board_size != 3:
                errors.append("El tamaño del tablero debe ser 3x3")
            if request.configuration.max_players != 2:
                errors.append("El número máximo de jugadores debe ser 2")
        
        return errors


class StartNewGameUseCaseFactory:
    """Factory para crear instancias del caso de uso StartNewGame."""
    
    @staticmethod
    def create() -> StartNewGameUseCase:
        """
        Crea una nueva instancia del caso de uso.
        
        Returns:
            Nueva instancia de StartNewGameUseCase
        """
        return StartNewGameUseCase()