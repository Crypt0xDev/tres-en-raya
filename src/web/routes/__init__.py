from flask import Blueprint

# Create a blueprint for the game routes
game_bp = Blueprint('game', __name__)

from .game_routes import *
from .api_routes import *