"""
Entidades del dominio del juego.

Este módulo exporta todas las entidades principales del dominio
que representan los conceptos fundamentales del juego Tres en Raya.
"""

from .board import Board, Position, Move, CellState, BoardSize
from .player import Player, PlayerType, PlayerSymbol, PlayerStats
from .game_session import GameSession, GameState, GameResult, GameConfiguration

__all__ = [
    # Board entities
    'Board',
    'Position', 
    'Move',
    'CellState',
    'BoardSize',
    
    # Player entities  
    'Player',
    'PlayerType',
    'PlayerSymbol',
    'PlayerStats',
    
    # Game session entities
    'GameSession',
    'GameState', 
    'GameResult',
    'GameConfiguration',
]
