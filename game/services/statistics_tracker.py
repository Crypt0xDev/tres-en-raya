"""
Servicio StatisticsTracker - Rastreador de Estadísticas para Tres en Raya.

Este servicio implementa el seguimiento y análisis de estadísticas del juego,
proporcionando métricas detalladas de rendimiento y tendencias.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from datetime import datetime, timedelta
from dataclasses import dataclass

from game.entities import Player, GameResult, GameSession


class StatisticsPeriod(Enum):
    """Períodos de tiempo para análisis estadístico."""
    TODAY = "today"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
    ALL_TIME = "all_time"


class TrendDirection(Enum):
    """Direcciones de tendencia en las estadísticas."""
    IMPROVING = "improving"
    DECLINING = "declining"
    STABLE = "stable"
    INSUFFICIENT_DATA = "insufficient_data"


@dataclass
class GameStatistics:
    """Estadísticas compiladas de juegos."""
    total_games: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    win_rate: float = 0.0
    average_game_duration: float = 0.0
    shortest_game: float = 0.0
    longest_game: float = 0.0
    games_per_day: float = 0.0


@dataclass
class PlayerTrend:
    """Tendencia de rendimiento de un jugador."""
    player_id: str
    player_name: str
    direction: TrendDirection
    change_percentage: float
    recent_performance: float
    historical_performance: float
    games_analyzed: int


class StatisticsTracker:
    """
    Servicio StatisticsTracker - Rastreador de estadísticas del dominio.
    
    Este servicio del dominio encapsula toda la lógica relacionada con
    el seguimiento, análisis y reporte de estadísticas del juego.
    
    Principios de Screaming Architecture aplicados:
    - Se enfoca en el DOMINIO: Estadísticas de Tres en Raya
    - Encapsula análisis de rendimiento de jugadores
    - No depende de frameworks externos
    - Utiliza entidades del dominio
    """
    
    def __init__(self):
        """Inicializa el rastreador de estadísticas."""
        pass
    
    def get_player_statistics(
        self, 
        player: Player, 
        period: StatisticsPeriod = StatisticsPeriod.ALL_TIME
    ) -> GameStatistics:
        """
        Obtiene las estadísticas de un jugador en un período específico.
        
        Args:
            player: Jugador del cual obtener estadísticas
            period: Período de tiempo a analizar
            
        Returns:
            Estadísticas compiladas del jugador
        """
        # En una implementación completa, aquí se consultarían los registros
        # de juegos del jugador filtrados por el período especificado
        
        stats = player.stats
        
        # Calcular estadísticas básicas
        total_games = stats.games_played
        wins = stats.games_won
        losses = stats.games_lost
        draws = stats.games_drawn
        
        win_rate = stats.win_rate if total_games > 0 else 0.0
        
        # Estimaciones para campos que requerirían datos históricos
        average_duration = self._estimate_average_duration(player)
        shortest_game = self._estimate_shortest_game(player)
        longest_game = self._estimate_longest_game(player)
        games_per_day = self._calculate_games_per_day(player)
        
        return GameStatistics(
            total_games=total_games,
            wins=wins,
            losses=losses,
            draws=draws,
            win_rate=win_rate,
            average_game_duration=average_duration,
            shortest_game=shortest_game,
            longest_game=longest_game,
            games_per_day=games_per_day
        )
    
    def analyze_player_trend(
        self, 
        player: Player,
        analysis_period: int = 10  # Últimos N juegos para análisis
    ) -> PlayerTrend:
        """
        Analiza la tendencia de rendimiento de un jugador.
        
        Args:
            player: Jugador a analizar
            analysis_period: Número de juegos recientes a considerar
            
        Returns:
            Análisis de tendencia del jugador
        """
        stats = player.stats
        
        if stats.games_played < 2:
            return PlayerTrend(
                player_id=player.id,
                player_name=player.name,
                direction=TrendDirection.INSUFFICIENT_DATA,
                change_percentage=0.0,
                recent_performance=0.0,
                historical_performance=0.0,
                games_analyzed=stats.games_played
            )
        
        # Simular análisis de tendencia basado en estadísticas disponibles
        recent_performance = stats.win_rate
        
        # Estimación de rendimiento histórico basado en patrones típicos
        historical_performance = self._estimate_historical_performance(player)
        
        # Calcular cambio porcentual
        if historical_performance > 0:
            change_percentage = ((recent_performance - historical_performance) / historical_performance) * 100
        else:
            change_percentage = 0.0
        
        # Determinar dirección de tendencia
        direction = self._determine_trend_direction(change_percentage)
        
        return PlayerTrend(
            player_id=player.id,
            player_name=player.name,
            direction=direction,
            change_percentage=change_percentage,
            recent_performance=recent_performance,
            historical_performance=historical_performance,
            games_analyzed=min(analysis_period, stats.games_played)
        )
    
    def get_global_statistics(self, all_players: List[Player]) -> Dict[str, Any]:
        """
        Genera estadísticas globales del sistema.
        
        Args:
            all_players: Lista de todos los jugadores del sistema
            
        Returns:
            Diccionario con estadísticas globales
        """
        if not all_players:
            return {
                "total_players": 0,
                "total_games": 0,
                "average_win_rate": 0.0,
                "most_active_player": None,
                "best_performer": None,
                "total_playtime_hours": 0.0
            }
        
        # Calcular estadísticas agregadas
        total_players = len(all_players)
        total_games = sum(player.stats.games_played for player in all_players)
        
        # Calcular tasa de victoria promedio
        win_rates = [player.stats.win_rate for player in all_players if player.stats.games_played > 0]
        average_win_rate = sum(win_rates) / len(win_rates) if win_rates else 0.0
        
        # Encontrar jugador más activo
        most_active_player = max(
            all_players, 
            key=lambda p: p.stats.games_played
        ) if all_players else None
        
        # Encontrar mejor jugador
        best_performer = max(
            all_players,
            key=lambda p: p.stats.win_rate if p.stats.games_played >= 5 else 0.0
        ) if all_players else None
        
        # Estimar tiempo total de juego
        estimated_playtime = self._estimate_total_playtime(all_players)
        
        return {
            "total_players": total_players,
            "total_games": total_games,
            "average_win_rate": round(average_win_rate, 2),
            "most_active_player": {
                "name": most_active_player.name,
                "games_played": most_active_player.stats.games_played
            } if most_active_player else None,
            "best_performer": {
                "name": best_performer.name,
                "win_rate": best_performer.stats.win_rate,
                "games_played": best_performer.stats.games_played
            } if best_performer else None,
            "total_playtime_hours": round(estimated_playtime, 2),
            "average_games_per_player": round(total_games / total_players, 2) if total_players > 0 else 0.0
        }
    
    def compare_players_detailed(self, player1: Player, player2: Player) -> Dict[str, Any]:
        """
        Realiza una comparación detallada entre dos jugadores.
        
        Args:
            player1: Primer jugador a comparar
            player2: Segundo jugador a comparar
            
        Returns:
            Análisis comparativo detallado
        """
        stats1 = self.get_player_statistics(player1)
        stats2 = self.get_player_statistics(player2)
        
        trend1 = self.analyze_player_trend(player1)
        trend2 = self.analyze_player_trend(player2)
        
        comparison = {
            "player1": {
                "name": player1.name,
                "statistics": stats1,
                "trend": trend1
            },
            "player2": {
                "name": player2.name,
                "statistics": stats2,
                "trend": trend2
            },
            "head_to_head": {
                "games_played_advantage": stats1.total_games - stats2.total_games,
                "win_rate_advantage": stats1.win_rate - stats2.win_rate,
                "efficiency_leader": player1.name if stats1.win_rate > stats2.win_rate else player2.name,
                "experience_leader": player1.name if stats1.total_games > stats2.total_games else player2.name,
                "trend_leader": self._determine_better_trend(trend1, trend2)
            },
            "recommendations": self._generate_player_recommendations(player1, player2, stats1, stats2)
        }
        
        return comparison
    
    def get_performance_insights(self, player: Player) -> Dict[str, Any]:
        """
        Genera insights de rendimiento para un jugador.
        
        Args:
            player: Jugador a analizar
            
        Returns:
            Insights y recomendaciones de rendimiento
        """
        stats = self.get_player_statistics(player)
        trend = self.analyze_player_trend(player)
        
        insights = {
            "current_level": self._assess_skill_level(stats),
            "strengths": self._identify_strengths(player, stats),
            "areas_for_improvement": self._identify_improvement_areas(player, stats),
            "trend_analysis": {
                "direction": trend.direction.value,
                "change_percentage": trend.change_percentage,
                "interpretation": self._interpret_trend(trend)
            },
            "milestones": self._identify_milestones(player, stats),
            "recommendations": self._generate_individual_recommendations(player, stats, trend)
        }
        
        return insights
    
    def calculate_activity_metrics(self, player: Player) -> Dict[str, Any]:
        """
        Calcula métricas de actividad del jugador.
        
        Args:
            player: Jugador a analizar
            
        Returns:
            Métricas de actividad y participación
        """
        stats = player.stats
        days_since_creation = (datetime.now() - player.created_at).days
        
        if days_since_creation == 0:
            days_since_creation = 1  # Evitar división por cero
        
        activity_metrics = {
            "days_active": days_since_creation,
            "games_per_day": stats.games_played / days_since_creation,
            "activity_level": self._classify_activity_level(stats.games_played, days_since_creation),
            "consistency_score": self._calculate_consistency_score(player),
            "engagement_level": self._assess_engagement_level(player),
            "last_activity": self._estimate_last_activity(player)
        }
        
        return activity_metrics
    
    def _estimate_average_duration(self, player: Player) -> float:
        """Estima la duración promedio de juegos basada en el tipo de jugador."""
        if player.is_ai:
            return 45.0  # Los juegos con IA suelen ser más rápidos
        else:
            return 120.0  # Juegos humanos promedio
    
    def _estimate_shortest_game(self, player: Player) -> float:
        """Estima el juego más corto."""
        return 15.0 if player.stats.games_played > 0 else 0.0
    
    def _estimate_longest_game(self, player: Player) -> float:
        """Estima el juego más largo."""
        return 300.0 if player.stats.games_played > 0 else 0.0
    
    def _calculate_games_per_day(self, player: Player) -> float:
        """Calcula juegos promedio por día."""
        days_since_creation = (datetime.now() - player.created_at).days
        if days_since_creation == 0:
            days_since_creation = 1
        
        return player.stats.games_played / days_since_creation
    
    def _estimate_historical_performance(self, player: Player) -> float:
        """Estima rendimiento histórico basado en patrones."""
        current_rate = player.stats.win_rate
        
        # Simulación de degradación típica del rendimiento inicial
        if player.stats.games_played < 10:
            return current_rate * 0.8  # Rendimiento inicial típicamente menor
        else:
            return current_rate * 0.95  # Ligera mejora histórica
    
    def _determine_trend_direction(self, change_percentage: float) -> TrendDirection:
        """Determina la dirección de la tendencia basada en el cambio porcentual."""
        if abs(change_percentage) < 5:
            return TrendDirection.STABLE
        elif change_percentage > 0:
            return TrendDirection.IMPROVING
        else:
            return TrendDirection.DECLINING
    
    def _estimate_total_playtime(self, players: List[Player]) -> float:
        """Estima el tiempo total de juego en horas."""
        total_games = sum(player.stats.games_played for player in players)
        average_game_duration_minutes = 2.0  # 2 minutos promedio por juego
        
        return (total_games * average_game_duration_minutes) / 60.0  # Convertir a horas
    
    def _determine_better_trend(self, trend1: PlayerTrend, trend2: PlayerTrend) -> str:
        """Determina qué jugador tiene mejor tendencia."""
        trend_scores = {
            TrendDirection.IMPROVING: 3,
            TrendDirection.STABLE: 2,
            TrendDirection.DECLINING: 1,
            TrendDirection.INSUFFICIENT_DATA: 0
        }
        
        score1 = trend_scores.get(trend1.direction, 0)
        score2 = trend_scores.get(trend2.direction, 0)
        
        if score1 > score2:
            return trend1.player_name
        elif score2 > score1:
            return trend2.player_name
        else:
            # Si empatan en tendencia, usar el cambio porcentual
            return trend1.player_name if trend1.change_percentage > trend2.change_percentage else trend2.player_name
    
    def _assess_skill_level(self, stats: GameStatistics) -> str:
        """Evalúa el nivel de habilidad basado en estadísticas."""
        if stats.total_games < 5:
            return "Novato"
        elif stats.win_rate >= 70:
            return "Experto"
        elif stats.win_rate >= 50:
            return "Intermedio"
        elif stats.win_rate >= 30:
            return "Principiante"
        else:
            return "En Desarrollo"
    
    def _identify_strengths(self, player: Player, stats: GameStatistics) -> List[str]:
        """Identifica las fortalezas del jugador."""
        strengths = []
        
        if stats.win_rate > 60:
            strengths.append("Alta tasa de victoria")
        
        if stats.games_per_day > 2:
            strengths.append("Jugador muy activo")
        
        if stats.total_games > 50:
            strengths.append("Experiencia considerable")
        
        if not strengths:
            strengths.append("Persistencia y dedicación")
        
        return strengths
    
    def _identify_improvement_areas(self, player: Player, stats: GameStatistics) -> List[str]:
        """Identifica áreas de mejora."""
        improvements = []
        
        if stats.win_rate < 40:
            improvements.append("Mejorar estrategia de juego")
        
        if stats.games_per_day < 0.5:
            improvements.append("Aumentar frecuencia de práctica")
        
        if stats.total_games < 10:
            improvements.append("Ganar más experiencia")
        
        return improvements
    
    def _interpret_trend(self, trend: PlayerTrend) -> str:
        """Interpreta la tendencia del jugador."""
        if trend.direction == TrendDirection.IMPROVING:
            return f"Mejorando consistentemente (+{trend.change_percentage:.1f}%)"
        elif trend.direction == TrendDirection.DECLINING:
            return f"Necesita atención ({trend.change_percentage:.1f}%)"
        elif trend.direction == TrendDirection.STABLE:
            return "Rendimiento estable y consistente"
        else:
            return "Necesita más juegos para análisis"
    
    def _identify_milestones(self, player: Player, stats: GameStatistics) -> List[str]:
        """Identifica hitos alcanzados o próximos."""
        milestones = []
        
        if stats.total_games >= 100:
            milestones.append("Veterano - 100+ juegos")
        elif stats.total_games >= 50:
            milestones.append("Experimentado - 50+ juegos")
        elif stats.total_games >= 10:
            milestones.append("Iniciado - 10+ juegos")
        
        if stats.win_rate >= 80:
            milestones.append("Maestro - 80%+ victorias")
        elif stats.win_rate >= 60:
            milestones.append("Experto - 60%+ victorias")
        
        return milestones
    
    def _generate_player_recommendations(
        self, 
        player1: Player, 
        player2: Player, 
        stats1: GameStatistics, 
        stats2: GameStatistics
    ) -> List[str]:
        """Genera recomendaciones basadas en la comparación."""
        recommendations = []
        
        if stats1.win_rate < stats2.win_rate:
            recommendations.append(f"{player1.name} podría aprender de las estrategias de {player2.name}")
        
        if stats1.games_per_day < stats2.games_per_day:
            recommendations.append(f"{player1.name} podría beneficiarse de más práctica regular")
        
        return recommendations
    
    def _generate_individual_recommendations(
        self, 
        player: Player, 
        stats: GameStatistics, 
        trend: PlayerTrend
    ) -> List[str]:
        """Genera recomendaciones individuales."""
        recommendations = []
        
        if stats.win_rate < 50:
            recommendations.append("Practica jugando contra la IA en dificultad fácil")
        
        if trend.direction == TrendDirection.DECLINING:
            recommendations.append("Considera revisar tus estrategias de juego")
        
        if stats.games_per_day < 1:
            recommendations.append("Juega al menos una partida diaria para mejorar")
        
        return recommendations
    
    def _classify_activity_level(self, games_played: int, days_active: int) -> str:
        """Clasifica el nivel de actividad del jugador."""
        games_per_day = games_played / days_active
        
        if games_per_day >= 3:
            return "Muy Activo"
        elif games_per_day >= 1:
            return "Activo"
        elif games_per_day >= 0.3:
            return "Moderado"
        else:
            return "Casual"
    
    def _calculate_consistency_score(self, player: Player) -> float:
        """Calcula un puntaje de consistencia (0-100)."""
        stats = player.stats
        
        if stats.games_played < 5:
            return 0.0
        
        # Simulación basada en la distribución de resultados
        total_results = stats.games_won + stats.games_lost + stats.games_drawn
        if total_results == 0:
            return 0.0
        
        # Consistencia basada en variación de resultados
        win_ratio = stats.games_won / total_results
        draw_ratio = stats.games_drawn / total_results
        loss_ratio = stats.games_lost / total_results
        
        # Calcular entropía como medida de consistencia
        ratios = [r for r in [win_ratio, draw_ratio, loss_ratio] if r > 0]
        entropy = -sum(r * (r ** 0.5) for r in ratios)  # Medida simplificada
        
        # Convertir a puntuación 0-100
        consistency = max(0, min(100, (1 - entropy) * 100))
        
        return round(consistency, 1)
    
    def _assess_engagement_level(self, player: Player) -> str:
        """Evalúa el nivel de compromiso del jugador."""
        days_since_creation = (datetime.now() - player.created_at).days
        games_per_day = player.stats.games_played / max(1, days_since_creation)
        
        if games_per_day >= 2 and player.stats.games_played >= 20:
            return "Altamente Comprometido"
        elif games_per_day >= 1 or player.stats.games_played >= 10:
            return "Comprometido"
        elif player.stats.games_played >= 5:
            return "Interesado"
        else:
            return "Explorando"
    
    def _estimate_last_activity(self, player: Player) -> str:
        """Estima la última actividad del jugador."""
        # En una implementación real, esto consultaría registros de actividad
        days_since_creation = (datetime.now() - player.created_at).days
        
        if days_since_creation <= 1:
            return "Hoy"
        elif days_since_creation <= 7:
            return "Esta semana"
        elif days_since_creation <= 30:
            return "Este mes"
        else:
            return "Hace más de un mes"