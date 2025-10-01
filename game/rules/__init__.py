"""
Reglas del dominio del juego.

Este módulo exporta todas las reglas y estrategias del dominio que definen
cómo se juega el Tres en Raya y qué constituye jugadas válidas.
"""

from .game_rules import GameRules, RuleViolationType, RuleViolation
from .victory_conditions import VictoryConditions, VictoryType, VictoryPattern
from .ai_strategy import (
    AIStrategyBase,
    AIStrategyFactory,
    StrategyType,
    DecisionWeight,
    RandomStrategy,
    DefensiveStrategy,
    AggressiveStrategy,
    MinimaxStrategy,
    StrategicStrategy
)

__all__ = [
    # Game Rules
    'GameRules',
    'RuleViolationType',
    'RuleViolation',
    
    # Victory Conditions
    'VictoryConditions', 
    'VictoryType',
    'VictoryPattern',
    
    # AI Strategies
    'AIStrategyBase',
    'AIStrategyFactory',
    'StrategyType',
    'DecisionWeight',
    'RandomStrategy',
    'DefensiveStrategy', 
    'AggressiveStrategy',
    'MinimaxStrategy',
    'StrategicStrategy',
]
