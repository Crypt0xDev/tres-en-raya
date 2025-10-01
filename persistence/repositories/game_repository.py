"""
Game Repository - Repositorio para gestionar sesiones de juego.

Este repositorio implementa el patrón Repository para abstraer
la persistencia de las sesiones de juego del dominio.
"""

from typing import Optional, List, Dict, Any
from game.entities import GameSession, GameState, GameResult, GameConfiguration
from game.entities import Player, PlayerType, PlayerSymbol
from persistence.data_sources.memory_storage import MemoryStorage


class GameRepository:
    """
    Repositorio para gestionar sesiones de juego.
    
    Implementa el patrón Repository para proporcionar una interfaz
    abstracta para el acceso a datos de sesiones de juego.
    
    Principios aplicados:
    - Abstrae la persistencia del dominio
    - Convierte entre entidades del dominio y datos persistidos
    - Encapsula la lógica de acceso a datos
    """
    
    COLLECTION_NAME = "game_sessions"
    
    def __init__(self, storage: MemoryStorage):
        """
        Inicializa el repositorio.
        
        Args:
            storage: Almacenamiento a utilizar
        """
        self._storage = storage
    
    def save(self, game_session: GameSession) -> bool:
        """
        Guarda una sesión de juego.
        
        Args:
            game_session: Sesión de juego a guardar
            
        Returns:
            True si se guardó exitosamente
        """
        try:
            data = self._serialize_game_session(game_session)
            return self._storage.save(
                self.COLLECTION_NAME, 
                game_session.id, 
                data
            )
        except Exception:
            return False
    
    def get_by_id(self, session_id: str) -> Optional[GameSession]:
        """
        Obtiene una sesión de juego por su ID.
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            Sesión de juego o None si no existe
        """
        try:
            data = self._storage.get(self.COLLECTION_NAME, session_id)
            if not data:
                return None
            
            return self._deserialize_game_session(data)
        except Exception:
            return None
    
    def get_all(self) -> List[GameSession]:
        """
        Obtiene todas las sesiones de juego.
        
        Returns:
            Lista de todas las sesiones
        """
        try:
            all_data = self._storage.get_all(self.COLLECTION_NAME)
            sessions = []
            
            for data in all_data:
                try:
                    session = self._deserialize_game_session(data)
                    if session:
                        sessions.append(session)
                except Exception:
                    continue  # Skip invalid sessions
            
            return sessions
        except Exception:
            return []
    
    def delete(self, session_id: str) -> bool:
        """
        Elimina una sesión de juego.
        
        Args:
            session_id: ID de la sesión a eliminar
            
        Returns:
            True si se eliminó exitosamente
        """
        return self._storage.delete(self.COLLECTION_NAME, session_id)
    
    def exists(self, session_id: str) -> bool:
        """
        Verifica si existe una sesión de juego.
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            True si la sesión existe
        """
        return self._storage.exists(self.COLLECTION_NAME, session_id)
    
    def find_by_player(self, player_id: str) -> List[GameSession]:
        """
        Busca sesiones que contengan un jugador específico.
        
        Args:
            player_id: ID del jugador
            
        Returns:
            Lista de sesiones que contienen al jugador
        """
        try:
            all_sessions = self.get_all()
            return [
                session for session in all_sessions
                if any(player.id == player_id for player in session.players)
            ]
        except Exception:
            return []
    
    def find_active_sessions(self) -> List[GameSession]:
        """
        Busca sesiones activas (en progreso o pausadas).
        
        Returns:
            Lista de sesiones activas
        """
        try:
            all_sessions = self.get_all()
            return [
                session for session in all_sessions
                if session.state in [GameState.IN_PROGRESS, GameState.PAUSED]
            ]
        except Exception:
            return []
    
    def count(self) -> int:
        """
        Cuenta el número total de sesiones.
        
        Returns:
            Número de sesiones
        """
        return self._storage.count(self.COLLECTION_NAME)
    
    def _serialize_game_session(self, game_session: GameSession) -> Dict[str, Any]:
        """
        Serializa una GameSession a diccionario.
        
        Args:
            game_session: Sesión a serializar
            
        Returns:
            Diccionario con los datos de la sesión
        """
        return {
            'id': game_session.id,
            'configuration': {
                'board_size': game_session.configuration.board_size,
                'max_players': game_session.configuration.max_players,
                'allow_ai_players': game_session.configuration.allow_ai_players,
                'time_limit_per_move': game_session.configuration.time_limit_per_move,
                'enable_statistics': game_session.configuration.enable_statistics
            },
            'state': game_session.state.value,
            'result': game_session.result.value if game_session.result else None,
            'current_player_symbol': game_session.current_player_symbol.value,
            'move_count': game_session.move_count,
            'created_at': game_session.created_at.isoformat(),
            'started_at': game_session.started_at.isoformat() if game_session.started_at else None,
            'finished_at': game_session.finished_at.isoformat() if game_session.finished_at else None,
            'board': game_session.board.to_list(),
            'move_history': [
                {
                    'position': {'row': move.position.row, 'col': move.position.col},
                    'player': move.player.value
                }
                for move in game_session.board.move_history
            ],
            'players': {
                'X': self._serialize_player(game_session.player_x) if game_session.player_x else None,
                'O': self._serialize_player(game_session.player_o) if game_session.player_o else None
            }
        }
    
    def _serialize_player(self, player: Player) -> Dict[str, Any]:
        """
        Serializa un Player a diccionario.
        
        Args:
            player: Jugador a serializar
            
        Returns:
            Diccionario con los datos del jugador
        """
        return {
            'id': player.id,
            'name': player.name,
            'player_type': player.player_type.value,
            'symbol': player.symbol.value if player.symbol else None,
            'stats': {
                'games_played': player.stats.games_played,
                'games_won': player.stats.games_won,
                'games_lost': player.stats.games_lost,
                'games_drawn': player.stats.games_drawn
            },
            'created_at': player.created_at.isoformat(),
            'is_active': player.is_active
        }
    
    def _deserialize_game_session(self, data: Dict[str, Any]) -> Optional[GameSession]:
        """
        Deserializa un diccionario a GameSession.
        
        Args:
            data: Datos a deserializar
            
        Returns:
            GameSession reconstruida o None si hay error
        """
        try:
            from datetime import datetime
            from game.entities import Position, Move, CellState, Board
            
            # Crear configuración
            config_data = data.get('configuration', {})
            configuration = GameConfiguration(
                board_size=config_data.get('board_size', 3),
                max_players=config_data.get('max_players', 2),
                allow_ai_players=config_data.get('allow_ai_players', True),
                time_limit_per_move=config_data.get('time_limit_per_move'),
                enable_statistics=config_data.get('enable_statistics', True)
            )
            
            # Crear sesión
            session = GameSession(
                configuration=configuration,
                session_id=data['id']
            )
            
            # Restaurar jugadores
            players_data = data.get('players', {})
            if players_data.get('X'):
                player_x = self._deserialize_player(players_data['X'])
                if player_x:
                    session.add_player(player_x, PlayerSymbol.X)
            
            if players_data.get('O'):
                player_o = self._deserialize_player(players_data['O'])
                if player_o:
                    session.add_player(player_o, PlayerSymbol.O)
            
            # Restaurar estado del juego (usando reflexión para acceder a atributos privados)
            session._state = GameState(data['state'])
            if data.get('result'):
                session._result = GameResult(data['result'])
            session._current_player_symbol = PlayerSymbol(data['current_player_symbol'])
            session._move_count = data['move_count']
            
            # Restaurar timestamps
            session._created_at = datetime.fromisoformat(data['created_at'])
            if data.get('started_at'):
                session._started_at = datetime.fromisoformat(data['started_at'])
            if data.get('finished_at'):
                session._finished_at = datetime.fromisoformat(data['finished_at'])
            
            # Restaurar tablero
            board_data = data.get('board', [])
            for row_idx, row in enumerate(board_data):
                for col_idx, cell in enumerate(row):
                    if cell != ' ':
                        cell_state = CellState.PLAYER_X if cell == 'X' else CellState.PLAYER_O
                        position = Position(row_idx, col_idx)
                        move = Move(position=position, player=cell_state)
                        session.board.place_move(move)
            
            return session
            
        except Exception:
            return None
    
    def _deserialize_player(self, data: Dict[str, Any]) -> Optional[Player]:
        """
        Deserializa un diccionario a Player.
        
        Args:
            data: Datos del jugador
            
        Returns:
            Player reconstruido o None si hay error
        """
        try:
            from datetime import datetime
            from game.entities import PlayerStats
            
            # Crear jugador
            player = Player(
                name=data['name'],
                player_type=PlayerType(data['player_type']),
                player_id=data['id']
            )
            
            # Asignar símbolo si existe
            if data.get('symbol'):
                player._symbol = PlayerSymbol(data['symbol'])
            
            # Restaurar estadísticas
            stats_data = data.get('stats', {})
            player._stats = PlayerStats(
                games_played=stats_data.get('games_played', 0),
                games_won=stats_data.get('games_won', 0),
                games_lost=stats_data.get('games_lost', 0),
                games_drawn=stats_data.get('games_drawn', 0)
            )
            
            # Restaurar timestamps y estado
            player._created_at = datetime.fromisoformat(data['created_at'])
            player._is_active = data.get('is_active', True)
            
            return player
            
        except Exception:
            return None