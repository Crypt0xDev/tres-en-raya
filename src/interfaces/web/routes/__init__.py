from flask import Blueprint

# Create a blueprint for the game routes
game_bp = Blueprint("game", __name__)

# Import route modules to register routes
from . import api_routes  # noqa: F401, E402
from . import game_routes  # noqa: F401, E402
