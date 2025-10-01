"""
Web Entry Point - Punto de entrada para la aplicación web.

Este módulo implementa el punto de entrada principal para ejecutar
el juego Tres en Raya como aplicación web usando Flask.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al PYTHONPATH
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
sys.path.insert(0, str(project_root))

# Importar después de configurar el PYTHONPATH
from interfaces.web_ui.flask_adapter import FlaskWebAdapter


class TicTacToeWebApp:
    """
    TicTacToeWebApp - Aplicación web para Tres en Raya.
    
    Esta clase de aplicación orquesta todos los componentes necesarios
    para ejecutar el juego como aplicación web siguiendo la
    Screaming Architecture.
    
    Principios aplicados:
    - Punto de entrada claro para el DOMINIO: Juego Tres en Raya Web
    - Orquestación de componentes sin lógica de negocio
    - Configuración basada en el entorno
    - Separación clara de responsabilidades
    """
    
    def __init__(self, environment: Environment = Environment.DEVELOPMENT):
        """
        Inicializa la aplicación web.
        
        Args:
            environment: Entorno de ejecución
        """
        self.config = get_configuration(environment)
        self.app = Flask(__name__)
        
        # Configurar Flask
        self._configure_flask()
        
        # Inicializar componentes de dominio
        self.storage = MemoryStorage()
        self.repository = GameRepository(self.storage)
        
        # Inicializar casos de uso
        self.start_game_use_case = StartNewGame(self.repository)
        self.make_move_use_case = MakeMove(self.repository)
        self.check_winner_use_case = CheckWinner(self.repository)
        self.manage_players_use_case = ManagePlayers(self.repository)
        
        # Inicializar adaptador web
        self.web_adapter = FlaskWebAdapter(
            app=self.app,
            start_game_use_case=self.start_game_use_case,
            make_move_use_case=self.make_move_use_case,
            check_winner_use_case=self.check_winner_use_case,
            manage_players_use_case=self.manage_players_use_case
        )
        
        # Registrar rutas
        self.web_adapter.register_routes()
    
    def _configure_flask(self) -> None:
        """Configura la aplicación Flask."""
        # Configuración de seguridad
        security = self.config.security_settings
        self.app.config['SECRET_KEY'] = security.secret_key
        self.app.config['SESSION_COOKIE_SECURE'] = security.session_cookie_secure
        self.app.config['SESSION_COOKIE_HTTPONLY'] = security.session_cookie_httponly
        self.app.config['SESSION_COOKIE_SAMESITE'] = security.session_cookie_samesite
        
        # Configuración de base de datos
        db = self.config.database_settings
        self.app.config['DATABASE_URI'] = db.uri
        
        # Configuración del servidor
        server = self.config.server_settings
        self.app.config['DEBUG'] = server.debug
        
        # Configuración específica del juego
        game = self.config.game_settings
        self.app.config['GAME_TITLE'] = game.title
        self.app.config['GAME_VERSION'] = game.version
        self.app.config['MAX_PLAYERS'] = game.max_players
        self.app.config['BOARD_SIZE'] = game.board_size
        
        # Configuración de JSON
        self.app.config['JSON_SORT_KEYS'] = False
        self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = server.debug
    
    def run(self) -> None:
        """
        Ejecuta la aplicación web.
        """
        server_config = self.config.server_settings
        
        print(f"🌐 Iniciando {self.config.game_settings.title} Web v{self.config.game_settings.version}")
        print(f"🏠 Servidor: http://{server_config.host}:{server_config.port}")
        print(f"🔧 Entorno: {self.config.environment.value}")
        print("=" * 60)
        
        try:
            self.app.run(
                host=server_config.host,
                port=server_config.port,
                debug=server_config.debug,
                threaded=server_config.threaded,
                processes=server_config.processes if not server_config.threaded else None
            )
        except KeyboardInterrupt:
            print("\n👋 Servidor detenido por el usuario")
        except Exception as e:
            print(f"\n❌ Error al iniciar el servidor: {e}")
            sys.exit(1)
    
    def get_flask_app(self) -> Flask:
        """
        Obtiene la instancia de Flask configurada.
        
        Returns:
            Instancia de Flask
        """
        return self.app


def create_app(environment: Optional[Environment] = None) -> Flask:
    """
    Factory function para crear la aplicación Flask.
    
    Args:
        environment: Entorno de ejecución (opcional)
        
    Returns:
        Instancia de Flask configurada
    """
    if environment is None:
        import os
        env_name = os.environ.get('FLASK_ENV', 'development').lower()
        environment = Environment(env_name) if env_name in [e.value for e in Environment] else Environment.DEVELOPMENT
    
    web_app = TicTacToeWebApp(environment)
    return web_app.get_flask_app()


def main() -> int:
    """
    Función principal para ejecutar la aplicación web.
    
    Returns:
        Código de salida
    """
    import argparse
    import os
    
    parser = argparse.ArgumentParser(
        description='Servidor web para el juego Tres en Raya'
    )
    
    parser.add_argument(
        '--env',
        choices=['development', 'testing', 'production'],
        default=None,
        help='Entorno de ejecución'
    )
    
    parser.add_argument(
        '--host',
        default=None,
        help='Host del servidor'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=None,
        help='Puerto del servidor'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Ejecutar en modo debug'
    )
    
    args = parser.parse_args()
    
    # Determinar entorno
    if args.env:
        environment = Environment(args.env)
    else:
        env_name = os.environ.get('FLASK_ENV', 'development').lower()
        environment = Environment(env_name) if env_name in [e.value for e in Environment] else Environment.DEVELOPMENT
    
    # Crear aplicación
    web_app = TicTacToeWebApp(environment)
    
    # Sobrescribir configuración con argumentos CLI si se proporcionan
    if args.host:
        web_app.config.server_settings = web_app.config.server_settings._replace(host=args.host)
    if args.port:
        web_app.config.server_settings = web_app.config.server_settings._replace(port=args.port)
    if args.debug:
        web_app.config.server_settings = web_app.config.server_settings._replace(debug=True)
    
    # Ejecutar aplicación
    try:
        web_app.run()
        return 0
    except Exception as e:
        print(f"Error fatal: {e}")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)