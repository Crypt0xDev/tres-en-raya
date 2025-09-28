import re
from functools import wraps

from flask import Blueprint, jsonify, request

api_routes = Blueprint("api_routes", __name__)


# Rate limiting decorators (to be applied when limiter is available)
def api_rate_limit(rate="60 per minute"):
    """Decorator factory for API rate limiting"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Rate limiting logic will be handled by Flask-Limiter
            return f(*args, **kwargs)

        # Store rate limit info for later application
        decorated_function._rate_limit = rate
        return decorated_function

    return decorator


def validate_json(f):
    """Decorator to validate JSON request data"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        return f(*args, **kwargs)

    return decorated_function


def validate_move_data(data):
    """Validate move data structure and values"""
    if not isinstance(data, dict):
        return False, "Invalid data format"

    # Check required fields
    required_fields = ["row", "col", "player"]
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    # Validate row and col are integers between 0-2
    try:
        row = int(data["row"])
        col = int(data["col"])
        if not (0 <= row <= 2) or not (0 <= col <= 2):
            return False, "Row and column must be between 0 and 2"
    except (ValueError, TypeError):
        return False, "Row and column must be valid integers"

    # Validate player is X or O
    player = data.get("player", "").upper()
    if player not in ["X", "O"]:
        return False, "Player must be 'X' or 'O'"

    return True, "Valid"


@api_routes.route("/start_game", methods=["POST"])
@api_rate_limit("10 per minute")
@validate_json
def start_game():
    """Start a new game with optional configuration"""
    try:
        data = request.get_json()

        # Default game configuration
        game_config = {"board_size": 3, "game_mode": "local", "first_player": "X"}

        # Validate and update configuration if provided
        if data:
            if "board_size" in data:
                size = data.get("board_size")
                if not isinstance(size, int) or size < 3 or size > 10:
                    return (
                        jsonify(
                            {"error": "Board size must be an integer between 3 and 10"}
                        ),
                        400,
                    )
                game_config["board_size"] = size

            if "game_mode" in data:
                mode = data.get("game_mode")
                if mode not in ["local", "multiplayer", "ai"]:
                    error_msg = "Game mode must be 'local', 'multiplayer', or 'ai'"
                    return (
                        jsonify({"error": error_msg}),
                        400,
                    )
                game_config["game_mode"] = mode

            if "first_player" in data:
                player = data.get("first_player", "").upper()
                if player not in ["X", "O"]:
                    error_msg = "First player must be 'X' or 'O'"
                    return jsonify({"error": error_msg}), 400
                game_config["first_player"] = player

        return (
            jsonify(
                {
                    "message": "Game started successfully!",
                    "game_id": "game_123",  # Generate unique ID in production
                    "config": game_config,
                }
            ),
            200,
        )

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@api_routes.route("/make_move", methods=["POST"])
@validate_json
def make_move():
    """Process a player's move with validation"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate move data
        is_valid, message = validate_move_data(data)
        if not is_valid:
            return jsonify({"error": message}), 400

        # Extract validated data
        row = int(data["row"])
        col = int(data["col"])
        player = data["player"].upper()
        game_id = data.get("game_id", "default")

        # Sanitize game_id to prevent injection
        if not re.match(r"^[a-zA-Z0-9_-]+$", game_id):
            return jsonify({"error": "Invalid game ID format"}), 400

        # Here you would add actual game logic
        # For now, return success with validated data
        return (
            jsonify(
                {
                    "message": "Move made successfully!",
                    "move": {
                        "row": row,
                        "col": col,
                        "player": player,
                        "game_id": game_id,
                    },
                }
            ),
            200,
        )

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@api_routes.route("/get_game_state", methods=["GET"])
def get_game_state():
    """Retrieve the current game state with validation"""
    try:
        # Validate game_id parameter if provided
        game_id = request.args.get("game_id", "default")

        # Sanitize game_id
        if not re.match(r"^[a-zA-Z0-9_-]+$", game_id):
            return jsonify({"error": "Invalid game ID format"}), 400

        # Mock game state - replace with actual logic
        game_state = {
            "game_id": game_id,
            "board": [["", "", ""], ["", "", ""], ["", "", ""]],
            "current_player": "X",
            "game_status": "in_progress",
            "winner": None,
            "moves_count": 0,
        }

        return jsonify({"game_state": game_state}), 200

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@api_routes.route("/end_game", methods=["POST"])
@validate_json
def end_game():
    """End the current game with optional reason"""
    try:
        data = request.get_json()

        # Validate game_id if provided
        game_id = data.get("game_id", "default") if data else "default"
        if not re.match(r"^[a-zA-Z0-9_-]+$", game_id):
            return jsonify({"error": "Invalid game ID format"}), 400

        # Validate end reason if provided
        end_reason = data.get("reason", "user_request") if data else "user_request"
        valid_reasons = ["user_request", "timeout", "disconnect", "winner", "draw"]
        if end_reason not in valid_reasons:
            return (
                jsonify(
                    {
                        "error": f"Invalid end reason. Must be one of: "
                                 f"{', '.join(valid_reasons)}"
                    }
                ),
                400,
            )

        return (
            jsonify(
                {
                    "message": "Game ended successfully!",
                    "game_id": game_id,
                    "reason": end_reason,
                }
            ),
            200,
        )

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@api_routes.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors"""
    return jsonify({"error": "Bad request"}), 400


@api_routes.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@api_routes.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors"""
    return jsonify({"error": "Internal server error"}), 500
