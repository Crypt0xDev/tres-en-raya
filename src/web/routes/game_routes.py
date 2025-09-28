from flask import Blueprint, request, jsonify
from ...core.game_engine import GameEngine

game_routes = Blueprint('game_routes', __name__)
game_engine = GameEngine()

@game_routes.route('/start', methods=['POST'])
def start_game():
    """Start a new game"""
    data = request.get_json() or {}
    player1_name = data.get('player1', 'Player 1')
    player2_name = data.get('player2', 'Player 2')
    
    game_id = game_engine.start_game(player1_name, player2_name)
    return jsonify({'game_id': game_id, 'status': 'Game started'}), 201

@game_routes.route('/status/<game_id>', methods=['GET'])
def game_status(game_id):
    """Get current game status"""
    status = game_engine.get_game_status(game_id)
    return jsonify(status), 200

@game_routes.route('/move', methods=['POST'])
def make_move():
    """Make a move in the game"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['game_id', 'player', 'position']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    result = game_engine.make_move(data['game_id'], data['player'], data['position'])
    return jsonify(result), 200

@game_routes.route('/end/<game_id>', methods=['POST'])
def end_game(game_id):
    """End a game"""
    result = game_engine.end_game(game_id)
    return jsonify(result), 200