"""
GameConfiguration - Configuración del juego Tres en Raya.

Este módulo maneja toda la configuración del juego siguiendo los principios
de Screaming Architecture, enfocándose en el dominio del negocio.
"""

import os
from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass
import json


class Environment(Enum):
    """Entornos de ejecución disponibles."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class GameMode(Enum):
    """Modos de juego disponibles."""
    LOCAL = "local"
    MULTIPLAYER = "multiplayer"
    AI_TRAINING = "ai_training"


@dataclass(frozen=True)
class GameSettings:
    """Configuración inmutable del juego."""
    title: str = "Tres en Raya"
    version: str = "2.0.0"
    max_players: int = 2
    board_size: int = 3
    win_condition: str = "3 in a row"
    enable_sound: bool = True
    enable_timer: bool = False
    timer_duration: int = 30


@dataclass(frozen=True)
class DatabaseSettings:
    """Configuración de base de datos."""
    uri: str
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10


@dataclass(frozen=True)
class SecuritySettings:
    """Configuración de seguridad."""
    secret_key: str
    session_cookie_secure: bool = True
    session_cookie_httponly: bool = True
    session_cookie_samesite: str = "Lax"
    csrf_enabled: bool = True


@dataclass(frozen=True)
class ServerSettings:
    """Configuración del servidor."""
    host: str = "127.0.0.1"
    port: int = 5000
    debug: bool = False
    threaded: bool = True
    processes: int = 1


class GameConfiguration:
    """
    GameConfiguration - Configuración centralizada del juego.
    
    Esta clase de infraestructura maneja toda la configuración del sistema
    siguiendo los principios de Screaming Architecture.
    
    Principios aplicados:
    - Configuración específica para el DOMINIO: Tres en Raya  
    - Separación clara entre configuración de juego y técnica
    - Inmutabilidad de configuraciones críticas
    - Fácil intercambio entre entornos
    """
    
    def __init__(self, environment: Environment = Environment.DEVELOPMENT):
        """
        Inicializa la configuración para el entorno especificado.
        
        Args:
            environment: Entorno de ejecución
        """
        self._environment = environment
        self._game_settings = self._load_game_settings()
        self._database_settings = self._load_database_settings()
        self._security_settings = self._load_security_settings()
        self._server_settings = self._load_server_settings()
    
    @property
    def environment(self) -> Environment:
        """Entorno actual de configuración."""
        return self._environment
    
    @property
    def game_settings(self) -> GameSettings:
        """Configuración específica del juego."""
        return self._game_settings
    
    @property
    def database_settings(self) -> DatabaseSettings:
        """Configuración de base de datos."""
        return self._database_settings
    
    @property
    def security_settings(self) -> SecuritySettings:
        """Configuración de seguridad."""
        return self._security_settings
    
    @property
    def server_settings(self) -> ServerSettings:
        """Configuración del servidor."""
        return self._server_settings
    
    def get_available_game_modes(self) -> List[GameMode]:
        """
        Obtiene los modos de juego disponibles según el entorno.
        
        Returns:
            Lista de modos de juego disponibles
        """
        if self._environment == Environment.PRODUCTION:
            return [GameMode.LOCAL, GameMode.MULTIPLAYER]
        else:
            return list(GameMode)  # Todos los modos en desarrollo/testing
    
    def get_default_player_names(self) -> List[str]:
        """
        Obtiene los nombres de jugador por defecto.
        
        Returns:
            Lista de nombres por defecto
        """
        return ["Jugador 1", "Jugador 2"]
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """
        Verifica si una característica está habilitada.
        
        Args:
            feature_name: Nombre de la característica
            
        Returns:
            True si está habilitada, False en caso contrario
        """
        feature_flags = {
            "ai_opponent": True,
            "statistics": True,
            "multiplayer": self._environment != Environment.TESTING,
            "sound_effects": self._game_settings.enable_sound,
            "game_timer": self._game_settings.enable_timer,
            "score_tracking": True,
            "player_profiles": True,
            "game_history": True,
        }
        
        return feature_flags.get(feature_name, False)
    
    def get_ai_difficulties(self) -> Dict[str, str]:
        """
        Obtiene las dificultades de IA disponibles.
        
        Returns:
            Diccionario de dificultades con descripciones
        """
        return {
            "easy": "Fácil - Movimientos aleatorios",
            "medium": "Medio - Estrategia defensiva",
            "hard": "Difícil - Algoritmo minimax"
        }
    
    def get_storage_path(self) -> str:
        """
        Obtiene la ruta de almacenamiento según el entorno.
        
        Returns:
            Ruta para archivos de datos
        """
        base_path = os.path.dirname(os.path.dirname(__file__))  # Volver al directorio raíz
        
        if self._environment == Environment.TESTING:
            return os.path.join(base_path, "data", "test")
        elif self._environment == Environment.PRODUCTION:
            return os.path.join(base_path, "data", "prod")
        else:
            return os.path.join(base_path, "data", "dev")
    
    def get_log_configuration(self) -> Dict[str, Any]:
        """
        Obtiene la configuración de logging según el entorno.
        
        Returns:
            Configuración de logging
        """
        if self._environment == Environment.PRODUCTION:
            return {
                "level": "WARNING",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "tic_tac_toe_prod.log",
                "max_size": "10MB",
                "backup_count": 5
            }
        elif self._environment == Environment.TESTING:
            return {
                "level": "CRITICAL",
                "format": "%(levelname)s - %(message)s",
                "file": None,  # Solo consola en testing
                "max_size": None,
                "backup_count": 0
            }
        else:  # Development
            return {
                "level": "DEBUG",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "tic_tac_toe_dev.log",
                "max_size": "5MB",
                "backup_count": 2
            }
    
    def _load_game_settings(self) -> GameSettings:
        """Carga configuración específica del juego."""
        # Intentar cargar desde archivo JSON personalizado
        config_file = self._get_config_file_path()
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    
                return GameSettings(
                    title=config_data.get("game_title", "Tres en Raya"),
                    version=config_data.get("version", "2.0.0"),
                    max_players=config_data.get("max_players", 2),
                    board_size=config_data.get("board_size", 3),
                    win_condition=config_data.get("win_condition", "3 in a row"),
                    enable_sound=config_data.get("settings", {}).get("enable_sound", True),
                    enable_timer=config_data.get("settings", {}).get("enable_timer", False),
                    timer_duration=config_data.get("settings", {}).get("timer_duration", 30)
                )
            except (json.JSONDecodeError, KeyError):
                pass  # Usar valores por defecto si hay error
        
        # Valores por defecto
        return GameSettings()
    
    def _load_database_settings(self) -> DatabaseSettings:
        """Carga configuración de base de datos."""
        if self._environment == Environment.PRODUCTION:
            return DatabaseSettings(
                uri=os.environ.get('DATABASE_URI', 'sqlite:///production.db'),
                echo=False,
                pool_size=10,
                max_overflow=20
            )
        elif self._environment == Environment.TESTING:
            return DatabaseSettings(
                uri='sqlite:///:memory:',  # Base de datos en memoria para tests
                echo=False,
                pool_size=1,
                max_overflow=0
            )
        else:  # Development
            return DatabaseSettings(
                uri='sqlite:///development.db',
                echo=True,  # SQL debug en desarrollo
                pool_size=5,
                max_overflow=10
            )
    
    def _load_security_settings(self) -> SecuritySettings:
        """Carga configuración de seguridad."""
        if self._environment == Environment.PRODUCTION:
            return SecuritySettings(
                secret_key=os.environ.get('SECRET_KEY', 'prod-secret-key-change-me'),
                session_cookie_secure=True,
                session_cookie_httponly=True,
                session_cookie_samesite="Strict",
                csrf_enabled=True
            )
        elif self._environment == Environment.TESTING:
            return SecuritySettings(
                secret_key='test-secret-key',
                session_cookie_secure=False,
                session_cookie_httponly=False,
                session_cookie_samesite="Lax",
                csrf_enabled=False
            )
        else:  # Development
            return SecuritySettings(
                secret_key='dev-secret-key',
                session_cookie_secure=False,
                session_cookie_httponly=True,
                session_cookie_samesite="Lax",
                csrf_enabled=False
            )
    
    def _load_server_settings(self) -> ServerSettings:
        """Carga configuración del servidor."""
        if self._environment == Environment.PRODUCTION:
            return ServerSettings(
                host=os.environ.get('HOST', '0.0.0.0'),
                port=int(os.environ.get('PORT', 5000)),
                debug=False,
                threaded=True,
                processes=4
            )
        elif self._environment == Environment.TESTING:
            return ServerSettings(
                host='127.0.0.1',
                port=0,  # Puerto aleatorio para tests
                debug=False,
                threaded=True,
                processes=1
            )
        else:  # Development
            return ServerSettings(
                host='127.0.0.1',
                port=5000,
                debug=True,
                threaded=True,
                processes=1
            )
    
    def _get_config_file_path(self) -> str:
        """Obtiene la ruta del archivo de configuración JSON."""
        base_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(base_path, "data", "config.json")


# Instancia global de configuración (Singleton pattern)
_config_instance: Optional[GameConfiguration] = None


def get_configuration(environment: Optional[Environment] = None) -> GameConfiguration:
    """
    Obtiene la instancia global de configuración.
    
    Args:
        environment: Entorno específico (opcional)
        
    Returns:
        Instancia de configuración
    """
    global _config_instance
    
    if _config_instance is None or (environment and _config_instance.environment != environment):
        # Determinar entorno si no se especifica
        if environment is None:
            env_name = os.environ.get('FLASK_ENV', 'development').lower()
            environment = Environment(env_name) if env_name in [e.value for e in Environment] else Environment.DEVELOPMENT
        
        _config_instance = GameConfiguration(environment)
    
    return _config_instance


def reset_configuration():
    """Reinicia la configuración global (útil para testing)."""
    global _config_instance
    _config_instance = None