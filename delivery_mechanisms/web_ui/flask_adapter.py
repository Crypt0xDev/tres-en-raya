"""
Adaptador Flask para la Interfaz Web del Juego Tres en Raya.

Este adaptador implementa el patrón Adapter para conectar Flask
(tecnología de delivery) con los casos de uso del dominio.
"""

from flask import Flask, render_template, request, jsonify, session as flask_session
from typing import Dict, Any, Optional
import uuid

from game.use_cases.start_new_game import (
    StartNewGameUseCase, StartNewGameRequest, StartNewGameUseCaseFactory
)
from game.use_cases.make_move import (
    MakeMoveUseCase, MakeMoveRequest, MakeMoveUseCaseFactory  
)
from game.entities import PlayerType, GameSession, Player
from persistence.repositories.game_repository import GameRepository
from persistence.data_sources.memory_storage import MemoryStorage


class FlaskWebAdapter:
    """
    Adaptador Flask que conecta la interfaz web con el dominio del juego.
    
    Este adaptador:
    - Recibe peticiones HTTP de la interfaz web
    - Las convierte a peticiones del dominio
    - Ejecuta casos de uso del dominio
    - Convierte respuestas del dominio a formato web
    
    Principios de Screaming Architecture:
    - Es un MECANISMO DE ENTREGA, no parte del dominio
    - Depende del dominio, no al revés
    - Traduce entre protocolo HTTP y casos de uso del negocio
    """
    
    def __init__(self):
        """Inicializa el adaptador Flask."""
        self.app = Flask(
            __name__,
            template_folder='templates',
            static_folder='.',
            static_url_path='/static'
        )
        self.app.secret_key = 'tres-en-raya-screaming-architecture'
        
        # Repositorio en memoria (puede ser inyectado)
        self._storage = MemoryStorage()
        self._game_repository = GameRepository(self._storage)
        
        # Casos de uso
        self._start_game_use_case = StartNewGameUseCaseFactory.create()
        self._make_move_use_case = MakeMoveUseCaseFactory.create(self._game_repository)
        
        # Configurar rutas
        self._setup_routes()
    
    def _setup_routes(self):
        """Configura las rutas de la aplicación Flask."""
        
        @self.app.route('/')
        def index():
            """Página principal del juego."""
            return render_template('index.html')
        
        @self.app.route('/api/game/start', methods=['POST'])
        def start_new_game():
            """API endpoint para iniciar una nueva partida."""
            try:
                data = request.get_json() or {}
                
                # Crear petición del caso de uso
                use_case_request = StartNewGameRequest(
                    player1_name=data.get('player1_name', 'Jugador 1'),
                    player2_name=data.get('player2_name'),
                    player2_type=self._parse_player_type(data.get('player2_type', 'human')),
                    session_id=str(uuid.uuid4())
                )
                
                # Ejecutar caso de uso
                response = self._start_game_use_case.execute(use_case_request)
                
                if response.success and response.game_session:
                    # Guardar sesión en repositorio
                    self._game_repository.save(response.game_session)
                    
                    # Guardar ID de sesión en la sesión web
                    flask_session['game_session_id'] = response.game_session.id
                    
                    return jsonify({
                        'success': True,
                        'message': response.message,
                        'game_session': self._serialize_game_session(response.game_session)
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': response.message,
                        'errors': response.errors
                    }), 400
                    
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': 'Error interno del servidor',
                    'errors': [str(e)]
                }), 500
        
        @self.app.route('/api/game/move', methods=['POST'])
        def make_move():
            """API endpoint para realizar un movimiento."""
            try:
                data = request.get_json() or {}
                game_session_id = flask_session.get('game_session_id') or data.get('game_session_id')
                
                if not game_session_id:
                    return jsonify({
                        'success': False,
                        'message': 'Sesión de juego no encontrada',
                        'errors': ['No hay una sesión de juego activa']
                    }), 400
                
                # Crear petición del caso de uso
                use_case_request = MakeMoveRequest(
                    game_session_id=game_session_id,
                    player_id=data.get('player_id', ''),
                    row=data.get('row', -1),
                    col=data.get('col', -1)
                )
                
                # Ejecutar caso de uso
                response = self._make_move_use_case.execute(use_case_request)
                
                result = {
                    'success': response.success,
                    'message': response.message,
                    'is_game_over': response.is_game_over,
                    'is_draw': response.is_draw,
                    'errors': response.errors
                }
                
                if response.game_session:
                    result['game_session'] = self._serialize_game_session(response.game_session)
                
                if response.winner:
                    result['winner'] = {
                        'id': response.winner.id,
                        'name': response.winner.name,
                        'symbol': response.winner.symbol.value if response.winner.symbol else None
                    }
                
                return jsonify(result)
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': 'Error interno del servidor',
                    'errors': [str(e)]
                }), 500
        
        @self.app.route('/api/game/status')
        def get_game_status():
            """API endpoint para obtener el estado actual del juego."""
            try:
                game_session_id = flask_session.get('game_session_id')
                
                if not game_session_id:
                    return jsonify({
                        'success': False,
                        'message': 'No hay sesión de juego activa',
                        'game_session': None
                    })
                
                game_session = self._game_repository.get_by_id(game_session_id)
                
                if not game_session:
                    return jsonify({
                        'success': False,
                        'message': 'Sesión de juego no encontrada',
                        'game_session': None
                    })
                
                return jsonify({
                    'success': True,
                    'message': 'Estado del juego obtenido',
                    'game_session': self._serialize_game_session(game_session)
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': 'Error interno del servidor',
                    'errors': [str(e)]
                }), 500
        
        @self.app.route('/api/game/reset', methods=['POST'])
        def reset_game():
            """API endpoint para reiniciar el juego."""
            try:
                game_session_id = flask_session.get('game_session_id')
                
                if not game_session_id:
                    return jsonify({
                        'success': False,
                        'message': 'No hay sesión de juego activa'
                    }), 400
                
                game_session = self._game_repository.get_by_id(game_session_id)
                
                if not game_session:
                    return jsonify({
                        'success': False,
                        'message': 'Sesión de juego no encontrada'
                    }), 404
                
                # Reiniciar el juego
                game_session.reset()
                self._game_repository.save(game_session)
                
                return jsonify({
                    'success': True,
                    'message': 'Juego reiniciado exitosamente',
                    'game_session': self._serialize_game_session(game_session)
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': 'Error interno del servidor',
                    'errors': [str(e)]
                }), 500
    
    def _parse_player_type(self, player_type_str: str) -> PlayerType:
        """
        Convierte string del tipo de jugador a enum PlayerType.
        
        Args:
            player_type_str: String del tipo de jugador
            
        Returns:
            PlayerType correspondiente
        """
        mapping = {
            'human': PlayerType.HUMAN,
            'ai_easy': PlayerType.AI_EASY,
            'ai_medium': PlayerType.AI_MEDIUM,
            'ai_hard': PlayerType.AI_HARD
        }
        return mapping.get(player_type_str.lower(), PlayerType.HUMAN)
    
    def _serialize_winner(self, winner: Optional[Player]) -> Optional[Dict[str, Any]]:
        """
        Serializa el jugador ganador.
        
        Args:
            winner: Jugador ganador o None
            
        Returns:
            Diccionario con datos del ganador o None
        """
        if not winner:
            return None
        
        return {
            'id': winner.id,
            'name': winner.name,
            'symbol': winner.symbol.value if winner.symbol else None
        }
    
    def _serialize_game_session(self, game_session: GameSession) -> Dict[str, Any]:
        """
        Serializa una GameSession a diccionario para JSON.
        
        Args:
            game_session: Sesión de juego a serializar
            
        Returns:
            Diccionario con los datos de la sesión
        """
        return {
            'id': game_session.id,
            'state': game_session.state.value,
            'result': game_session.result.value if game_session.result else None,
            'board': game_session.board.to_list(),
            'current_player': {
                'id': game_session.current_player.id,
                'name': game_session.current_player.name,
                'symbol': game_session.current_player_symbol.value
            } if game_session.current_player else None,
            'players': [
                {
                    'id': player.id,
                    'name': player.name,
                    'symbol': player.symbol.value if player.symbol else None,
                    'type': player.player_type.value,
                    'stats': {
                        'games_played': player.stats.games_played,
                        'games_won': player.stats.games_won,
                        'games_lost': player.stats.games_lost,
                        'games_drawn': player.stats.games_drawn,
                        'win_rate': player.stats.win_rate
                    }
                }
                for player in game_session.players
            ],
            'move_count': game_session.move_count,
            'is_finished': game_session.is_finished(),
            'is_draw': game_session.is_draw(),
            'winner': self._serialize_winner(game_session.get_winner()) if game_session.get_winner() else None,
            'available_moves': [
                {'row': pos.row, 'col': pos.col} 
                for pos in game_session.get_available_moves()
            ],
            'created_at': game_session.created_at.isoformat() if game_session.created_at else None,
            'started_at': game_session.started_at.isoformat() if game_session.started_at else None,
            'finished_at': game_session.finished_at.isoformat() if game_session.finished_at else None
        }
    
    def run(self, debug: bool = True, host: str = '127.0.0.1', port: int = 5000):
        """
        Ejecuta la aplicación Flask.
        
        Args:
            debug: Modo debug
            host: Host de la aplicación
            port: Puerto de la aplicación
        """
        self.app.run(debug=debug, host=host, port=port)