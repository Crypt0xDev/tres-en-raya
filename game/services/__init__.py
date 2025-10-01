"""
Servicios del dominio del juego.

Este módulo exporta todos los servicios del dominio que encapsulan
la lógica de negocio compleja y coordinan las operaciones entre entidades.
"""

from .ai_opponent import AIOpponent, AIStrategy, AIDifficulty
from .score_calculator import ScoreCalculator, ScoreType, PerformanceRating
from .statistics_tracker import (
    StatisticsTracker, 
    StatisticsPeriod, 
    TrendDirection, 
    GameStatistics, 
    PlayerTrend
)

__all__ = [
    # AI Opponent service
    'AIOpponent',
    'AIStrategy', 
    'AIDifficulty',
    
    # Score Calculator service
    'ScoreCalculator',
    'ScoreType',
    'PerformanceRating',
    
    # Statistics Tracker service
    'StatisticsTracker',
    'StatisticsPeriod',
    'TrendDirection', 
    'GameStatistics',
    'PlayerTrend',
]