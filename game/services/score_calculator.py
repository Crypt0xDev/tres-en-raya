"""
Servicio ScoreCalculator - Calculadora de Puntuaciones para Tres en Raya.

Este servicio implementa la lógica de cálculo de puntuaciones, ranking
y métricas de desempeño para jugadores.
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime

from game.entities import Player, PlayerType, GameResult


class ScoreType(Enum):
    """Tipos de puntuación disponibles."""
    WIN = "win"
    DRAW = "draw" 
    LOSS = "loss"


class PerformanceRating(Enum):
    """Clasificaciones de rendimiento."""
    BEGINNER = "beginner"      # 0-199 puntos
    AMATEUR = "amateur"        # 200-399 puntos
    INTERMEDIATE = "intermediate"  # 400-699 puntos
    ADVANCED = "advanced"      # 700-999 puntos
    EXPERT = "expert"          # 1000+ puntos


class ScoreCalculator:
    """
    Servicio ScoreCalculator - Calculadora de puntuaciones del dominio.
    
    Este servicio del dominio encapsula toda la lógica relacionada con
    el cálculo de puntuaciones, rankings y métricas de rendimiento
    en el juego de Tres en Raya.
    
    Principios de Screaming Architecture aplicados:
    - Se enfoca en el DOMINIO: Cálculo de puntuaciones de Tres en Raya
    - Encapsula reglas de puntuación del juego
    - No depende de frameworks externos
    - Utiliza entidades del dominio
    """
    
    # Constantes de puntuación
    WIN_POINTS = 100
    DRAW_POINTS = 30
    LOSS_POINTS = 0
    
    def __init__(self):
        """Inicializa el calculador de puntuaciones."""
        pass
    
    def calculate_game_score(
        self, 
        player: Player, 
        result: GameResult, 
        opponent_type: PlayerType,
        ai_difficulty: Optional[str] = None,
        game_duration: Optional[int] = None
    ) -> int:
        """
        Calcula la puntuación obtenida en un juego individual.
        
        Args:
            player: Jugador que obtuvo el resultado
            result: Resultado del juego
            opponent_type: Tipo de oponente
            ai_difficulty: Dificultad de la IA si aplica
            game_duration: Duración del juego en segundos
            
        Returns:
            Puntos obtenidos en el juego
        """
        base_score = self._get_base_score(result)
        
        # Multiplicador por tipo de oponente
        opponent_multiplier = 1.0
        if opponent_type in [PlayerType.AI_EASY, PlayerType.AI_MEDIUM, PlayerType.AI_HARD]:
            if ai_difficulty == "easy":
                opponent_multiplier = 1.0
            elif ai_difficulty == "medium":
                opponent_multiplier = 1.2
            elif ai_difficulty == "hard":
                opponent_multiplier = 1.5
        elif opponent_type == PlayerType.HUMAN:
            opponent_multiplier = 1.1  # Bonificación por jugar contra humanos
        
        # Bonificación por velocidad (solo para victorias)
        speed_bonus = 0
        if result in [GameResult.PLAYER_X_WINS, GameResult.PLAYER_O_WINS] and game_duration:
            speed_bonus = self._calculate_speed_bonus(game_duration)
        
        # Cálculo final
        total_score = int((base_score * opponent_multiplier) + speed_bonus)
        
        return max(0, total_score)  # No permitir puntuaciones negativas
    
    def calculate_total_score(self, player: Player) -> int:
        """
        Calcula la puntuación total acumulada de un jugador.
        
        Args:
            player: Jugador del cual calcular la puntuación
            
        Returns:
            Puntuación total del jugador
        """
        stats = player.stats
        
        # Puntuación base por resultados
        total_score = (
            (stats.games_won * self.WIN_POINTS) +
            (stats.games_drawn * self.DRAW_POINTS) +
            (stats.games_lost * self.LOSS_POINTS)
        )
        
        return max(0, total_score)
    
    def get_performance_rating(self, total_score: int) -> PerformanceRating:
        """
        Determina la clasificación de rendimiento basada en la puntuación.
        
        Args:
            total_score: Puntuación total del jugador
            
        Returns:
            Clasificación de rendimiento
        """
        if total_score >= 1000:
            return PerformanceRating.EXPERT
        elif total_score >= 700:
            return PerformanceRating.ADVANCED
        elif total_score >= 400:
            return PerformanceRating.INTERMEDIATE
        elif total_score >= 200:
            return PerformanceRating.AMATEUR
        else:
            return PerformanceRating.BEGINNER
    
    def calculate_win_rate(self, player: Player) -> float:
        """
        Calcula el porcentaje de victorias del jugador.
        
        Args:
            player: Jugador del cual calcular la tasa de victorias
            
        Returns:
            Porcentaje de victorias (0.0 a 100.0)
        """
        return player.stats.win_rate
    
    def calculate_efficiency_rating(self, player: Player) -> float:
        """
        Calcula una calificación de eficiencia del jugador.
        
        La eficiencia considera victorias, empates y derrotas con diferentes pesos.
        
        Args:
            player: Jugador del cual calcular la eficiencia
            
        Returns:
            Calificación de eficiencia (0.0 a 100.0)
        """
        stats = player.stats
        total_games = stats.games_played
        
        if total_games == 0:
            return 0.0
        
        # Pesos para diferentes resultados
        win_weight = 1.0
        draw_weight = 0.5
        loss_weight = 0.0
        
        weighted_score = (
            (stats.games_won * win_weight) +
            (stats.games_drawn * draw_weight) +
            (stats.games_lost * loss_weight)
        )
        
        efficiency = (weighted_score / total_games) * 100
        return round(efficiency, 2)
    
    def get_ranking_position(self, player: Player, all_players: List[Player]) -> int:
        """
        Determina la posición del jugador en el ranking global.
        
        Args:
            player: Jugador a evaluar
            all_players: Lista de todos los jugadores
            
        Returns:
            Posición en el ranking (1 = primer lugar)
        """
        # Calcular puntuaciones de todos los jugadores
        player_scores = []
        for p in all_players:
            score = self.calculate_total_score(p)
            player_scores.append((p.id, score))
        
        # Ordenar por puntuación descendente
        player_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Encontrar posición del jugador
        for position, (player_id, _) in enumerate(player_scores, 1):
            if player_id == player.id:
                return position
        
        return len(all_players)  # Si no se encontró, última posición
    
    def get_performance_summary(self, player: Player) -> Dict[str, Any]:
        """
        Genera un resumen completo del rendimiento del jugador.
        
        Args:
            player: Jugador del cual generar el resumen
            
        Returns:
            Diccionario con métricas de rendimiento
        """
        total_score = self.calculate_total_score(player)
        rating = self.get_performance_rating(total_score)
        win_rate = self.calculate_win_rate(player)
        efficiency = self.calculate_efficiency_rating(player)
        
        summary = {
            "player_name": player.name,
            "total_score": total_score,
            "performance_rating": rating.value,
            "win_rate_percentage": win_rate,
            "efficiency_rating": efficiency,
            "games_played": player.stats.games_played,
            "wins": player.stats.games_won,
            "draws": player.stats.games_drawn,
            "losses": player.stats.games_lost,
            "created_at": player.created_at.isoformat()
        }
        
        return summary
    
    def compare_players(self, player1: Player, player2: Player) -> Dict[str, Any]:
        """
        Compara las estadísticas de dos jugadores.
        
        Args:
            player1: Primer jugador
            player2: Segundo jugador
            
        Returns:
            Diccionario con la comparación detallada
        """
        summary1 = self.get_performance_summary(player1)
        summary2 = self.get_performance_summary(player2)
        
        comparison = {
            "player1": summary1,
            "player2": summary2,
            "better_total_score": player1.name if summary1["total_score"] > summary2["total_score"] else player2.name,
            "better_win_rate": player1.name if summary1["win_rate_percentage"] > summary2["win_rate_percentage"] else player2.name,
            "better_efficiency": player1.name if summary1["efficiency_rating"] > summary2["efficiency_rating"] else player2.name,
            "score_difference": abs(summary1["total_score"] - summary2["total_score"]),
            "win_rate_difference": abs(summary1["win_rate_percentage"] - summary2["win_rate_percentage"]),
            "efficiency_difference": abs(summary1["efficiency_rating"] - summary2["efficiency_rating"])
        }
        
        return comparison
    
    def _get_base_score(self, result: GameResult) -> int:
        """
        Obtiene la puntuación base según el resultado.
        
        Args:
            result: Resultado del juego
            
        Returns:
            Puntuación base
        """
        if result in [GameResult.PLAYER_X_WINS, GameResult.PLAYER_O_WINS]:
            return self.WIN_POINTS
        elif result == GameResult.DRAW:
            return self.DRAW_POINTS
        else:
            return self.LOSS_POINTS
    
    def _calculate_speed_bonus(self, game_duration: int) -> int:
        """
        Calcula bonificación por velocidad de juego.
        
        Args:
            game_duration: Duración del juego en segundos
            
        Returns:
            Puntos de bonificación por velocidad
        """
        # Bonificación por juegos rápidos (menos de 30 segundos)
        if game_duration <= 30:
            return 20
        elif game_duration <= 60:
            return 10
        elif game_duration <= 120:
            return 5
        else:
            return 0
    
    def _calculate_speed_bonus(self, game_duration: int) -> int:
        """
        Calcula bonificación por velocidad de juego.
        
        Args:
            game_duration: Duración del juego en segundos
            
        Returns:
            Puntos de bonificación por velocidad
        """
        # Bonificación por juegos rápidos (menos de 30 segundos)
        if game_duration <= 30:
            return 20
        elif game_duration <= 60:
            return 10
        elif game_duration <= 120:
            return 5
        else:
            return 0
    
    def _get_total_games(self, player: Player) -> int:
        """
        Obtiene el total de juegos jugados por el jugador.
        
        Args:
            player: Jugador a evaluar
            
        Returns:
            Número total de juegos
        """
        if not player.statistics:
            return 0
        
        stats = player.statistics
        return stats.wins + stats.draws + stats.losses
    
    def _calculate_points_per_game(self, player: Player) -> float:
        """
        Calcula los puntos promedio por juego.
        
        Args:
            player: Jugador a evaluar
            
        Returns:
            Puntos promedio por juego
        """
        total_games = self._get_total_games(player)
        if total_games == 0:
            return 0.0
        
        total_score = self.calculate_total_score(player)
        return round(total_score / total_games, 2)