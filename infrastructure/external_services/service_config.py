"""
ExternalServices - Configuración de servicios externos.

Este módulo maneja la configuración de servicios externos que podría
usar el juego Tres en Raya, como APIs, bases de datos remotas, etc.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import os


class ServiceStatus(Enum):
    """Estados de servicios externos."""
    ENABLED = "enabled"
    DISABLED = "disabled"
    MAINTENANCE = "maintenance"


@dataclass(frozen=True)
class APIConfiguration:
    """Configuración para APIs externas."""
    base_url: str
    api_key: Optional[str] = None
    timeout: int = 30
    retry_attempts: int = 3
    rate_limit: int = 100  # requests per minute


@dataclass(frozen=True)
class DatabaseConfiguration:
    """Configuración de base de datos externa."""
    host: str
    port: int
    database: str
    username: str
    password: str
    ssl_enabled: bool = True
    connection_pool_size: int = 10


class ExternalServicesConfiguration:
    """
    ExternalServicesConfiguration - Configuración de servicios externos.
    
    Esta clase de infraestructura maneja la configuración de todos los
    servicios externos que el juego podría necesitar.
    
    Principios de Screaming Architecture aplicados:
    - Aislamiento de dependencias externas
    - Configuración específica para servicios del dominio
    - Fácil intercambio y deshabilitación de servicios
    """
    
    def __init__(self):
        """Inicializa la configuración de servicios externos."""
        self._services_status = self._load_services_status()
        self._api_configurations = self._load_api_configurations()
        self._database_configurations = self._load_database_configurations()
    
    def is_service_enabled(self, service_name: str) -> bool:
        """
        Verifica si un servicio está habilitado.
        
        Args:
            service_name: Nombre del servicio
            
        Returns:
            True si está habilitado, False en caso contrario
        """
        status = self._services_status.get(service_name, ServiceStatus.DISABLED)
        return status == ServiceStatus.ENABLED
    
    def get_api_configuration(self, api_name: str) -> Optional[APIConfiguration]:
        """
        Obtiene la configuración de una API específica.
        
        Args:
            api_name: Nombre de la API
            
        Returns:
            Configuración de la API o None si no existe
        """
        return self._api_configurations.get(api_name)
    
    def get_database_configuration(self, db_name: str) -> Optional[DatabaseConfiguration]:
        """
        Obtiene la configuración de una base de datos específica.
        
        Args:
            db_name: Nombre de la base de datos
            
        Returns:
            Configuración de la base de datos o None si no existe
        """
        return self._database_configurations.get(db_name)
    
    def get_leaderboard_api_config(self) -> Optional[APIConfiguration]:
        """
        Obtiene configuración para API de tabla de clasificación.
        
        Returns:
            Configuración de API de leaderboard
        """
        return self.get_api_configuration("leaderboard")
    
    def get_statistics_api_config(self) -> Optional[APIConfiguration]:
        """
        Obtiene configuración para API de estadísticas.
        
        Returns:
            Configuración de API de estadísticas
        """
        return self.get_api_configuration("statistics")
    
    def get_notification_config(self) -> Dict[str, Any]:
        """
        Obtiene configuración para notificaciones.
        
        Returns:
            Configuración de sistema de notificaciones
        """
        return {
            "email_enabled": self.is_service_enabled("email_notifications"),
            "push_enabled": self.is_service_enabled("push_notifications"),
            "smtp_server": os.environ.get("SMTP_SERVER", "localhost"),
            "smtp_port": int(os.environ.get("SMTP_PORT", 587)),
            "smtp_username": os.environ.get("SMTP_USERNAME"),
            "smtp_password": os.environ.get("SMTP_PASSWORD"),
        }
    
    def get_analytics_config(self) -> Dict[str, Any]:
        """
        Obtiene configuración para analytics.
        
        Returns:
            Configuración de analytics
        """
        return {
            "enabled": self.is_service_enabled("analytics"),
            "google_analytics_id": os.environ.get("GA_TRACKING_ID"),
            "custom_analytics_endpoint": os.environ.get("ANALYTICS_ENDPOINT"),
            "track_game_events": True,
            "track_user_actions": True,
            "privacy_mode": os.environ.get("PRIVACY_MODE", "standard")
        }
    
    def get_multiplayer_server_config(self) -> Dict[str, Any]:
        """
        Obtiene configuración para servidor multijugador.
        
        Returns:
            Configuración del servidor multijugador
        """
        return {
            "enabled": self.is_service_enabled("multiplayer_server"),
            "websocket_url": os.environ.get("WEBSOCKET_URL", "ws://localhost:8080"),
            "max_connections": int(os.environ.get("MAX_CONNECTIONS", 100)),
            "heartbeat_interval": int(os.environ.get("HEARTBEAT_INTERVAL", 30)),
            "room_timeout": int(os.environ.get("ROOM_TIMEOUT", 300)),
            "enable_reconnection": True,
            "reconnection_timeout": 60
        }
    
    def _load_services_status(self) -> Dict[str, ServiceStatus]:
        """Carga el estado de los servicios."""
        # En una implementación real, esto podría venir de un archivo de configuración
        # o variables de entorno
        
        environment = os.environ.get("FLASK_ENV", "development")
        
        if environment == "production":
            return {
                "leaderboard": ServiceStatus.ENABLED,
                "statistics": ServiceStatus.ENABLED,
                "email_notifications": ServiceStatus.ENABLED,
                "push_notifications": ServiceStatus.ENABLED,
                "analytics": ServiceStatus.ENABLED,
                "multiplayer_server": ServiceStatus.ENABLED,
                "external_database": ServiceStatus.ENABLED,
                "cache_service": ServiceStatus.ENABLED,
                "backup_service": ServiceStatus.ENABLED
            }
        elif environment == "testing":
            return {
                # En testing, la mayoría de servicios externos están deshabilitados
                "leaderboard": ServiceStatus.DISABLED,
                "statistics": ServiceStatus.DISABLED,
                "email_notifications": ServiceStatus.DISABLED,
                "push_notifications": ServiceStatus.DISABLED,
                "analytics": ServiceStatus.DISABLED,
                "multiplayer_server": ServiceStatus.DISABLED,
                "external_database": ServiceStatus.DISABLED,
                "cache_service": ServiceStatus.DISABLED,
                "backup_service": ServiceStatus.DISABLED
            }
        else:  # development
            return {
                "leaderboard": ServiceStatus.ENABLED,
                "statistics": ServiceStatus.ENABLED,
                "email_notifications": ServiceStatus.DISABLED,
                "push_notifications": ServiceStatus.DISABLED,
                "analytics": ServiceStatus.DISABLED,
                "multiplayer_server": ServiceStatus.ENABLED,
                "external_database": ServiceStatus.DISABLED,
                "cache_service": ServiceStatus.DISABLED,
                "backup_service": ServiceStatus.DISABLED
            }
    
    def _load_api_configurations(self) -> Dict[str, APIConfiguration]:
        """Carga configuraciones de APIs."""
        configs = {}
        
        # API de Leaderboard
        leaderboard_url = os.environ.get("LEADERBOARD_API_URL")
        if leaderboard_url:
            configs["leaderboard"] = APIConfiguration(
                base_url=leaderboard_url,
                api_key=os.environ.get("LEADERBOARD_API_KEY"),
                timeout=30,
                retry_attempts=3,
                rate_limit=60
            )
        
        # API de Estadísticas
        statistics_url = os.environ.get("STATISTICS_API_URL")
        if statistics_url:
            configs["statistics"] = APIConfiguration(
                base_url=statistics_url,
                api_key=os.environ.get("STATISTICS_API_KEY"),
                timeout=20,
                retry_attempts=2,
                rate_limit=100
            )
        
        # API de Juegos en línea
        online_games_url = os.environ.get("ONLINE_GAMES_API_URL")
        if online_games_url:
            configs["online_games"] = APIConfiguration(
                base_url=online_games_url,
                api_key=os.environ.get("ONLINE_GAMES_API_KEY"),
                timeout=10,
                retry_attempts=1,
                rate_limit=200
            )
        
        return configs
    
    def _load_database_configurations(self) -> Dict[str, DatabaseConfiguration]:
        """Carga configuraciones de bases de datos externas."""
        configs = {}
        
        # Base de datos de estadísticas
        stats_db_host = os.environ.get("STATS_DB_HOST")
        stats_db_port = os.environ.get("STATS_DB_PORT")
        stats_db_name = os.environ.get("STATS_DB_NAME")
        stats_db_user = os.environ.get("STATS_DB_USER")
        stats_db_password = os.environ.get("STATS_DB_PASSWORD")
        
        if all([stats_db_host, stats_db_port, stats_db_name, stats_db_user, stats_db_password]):
            configs["statistics"] = DatabaseConfiguration(
                host=stats_db_host,
                port=int(stats_db_port),
                database=stats_db_name,
                username=stats_db_user,
                password=stats_db_password,
                ssl_enabled=os.environ.get("STATS_DB_SSL", "true").lower() == "true",
                connection_pool_size=int(os.environ.get("STATS_DB_POOL_SIZE", "10"))
            )
        
        # Base de datos de usuarios
        user_db_host = os.environ.get("USER_DB_HOST")
        user_db_port = os.environ.get("USER_DB_PORT")
        user_db_name = os.environ.get("USER_DB_NAME")
        user_db_user = os.environ.get("USER_DB_USER")
        user_db_password = os.environ.get("USER_DB_PASSWORD")
        
        if all([user_db_host, user_db_port, user_db_name, user_db_user, user_db_password]):
            configs["users"] = DatabaseConfiguration(
                host=user_db_host,
                port=int(user_db_port),
                database=user_db_name,
                username=user_db_user,
                password=user_db_password,
                ssl_enabled=os.environ.get("USER_DB_SSL", "true").lower() == "true",
                connection_pool_size=int(os.environ.get("USER_DB_POOL_SIZE", "5"))
            )
        
        return configs


# Instancia global (Singleton)
_external_services_instance: Optional[ExternalServicesConfiguration] = None


def get_external_services_configuration() -> ExternalServicesConfiguration:
    """
    Obtiene la instancia global de configuración de servicios externos.
    
    Returns:
        Instancia de configuración de servicios externos
    """
    global _external_services_instance
    
    if _external_services_instance is None:
        _external_services_instance = ExternalServicesConfiguration()
    
    return _external_services_instance


def reset_external_services_configuration():
    """Reinicia la configuración de servicios externos (útil para testing)."""
    global _external_services_instance
    _external_services_instance = None