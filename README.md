# Tres en Raya Game

## Descripción
Tres en Raya es un juego clásico de estrategia en el que dos jugadores se turnan para marcar espacios en una cuadrícula de 3x3. El objetivo es ser el primero en alinear tres de sus marcas en una fila, columna o diagonal.

Este proyecto incluye tres modos de juego:
- **Juego Local**: Para dos jugadores en la misma terminal
- **Juego Web**: Interfaz web con navegador
- **Juego Multijugador**: Con servidor Socket.IO

## Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd tres-en-raya-game
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Instalar el paquete
```bash
pip install -e .
```

## Uso

### Juego Local (Terminal)
```bash
tres-en-raya-local
# O directamente:
python -m src.local.main
```

### Juego Web
```bash
tres-en-raya-web
# O directamente:
python -m src.web.app
```
Luego abre http://localhost:5000 en tu navegador.

### Servidor Multijugador
```bash
tres-en-raya-multiplayer
# O directamente:
python -m src.multiplayer.server
```

## Estructura del Proyecto

- **src/**: Código fuente del juego
  - **core/**: Módulos principales
    - `board.py`: Lógica del tablero
    - `game_engine.py`: Motor del juego
    - `player.py`: Gestión de jugadores
  - **local/**: Versión para terminal
    - `main.py`: Punto de entrada local
    - `game_logic.py`: Lógica específica local
    - **ui/**: Interfaz de consola
  - **web/**: Versión web (Flask)
    - `app.py`: Servidor Flask
    - **routes/**: Rutas del servidor
    - **templates/**: Plantillas HTML
    - **static/**: CSS y JavaScript
  - **multiplayer/**: Versión multijugador
    - `server.py`: Servidor Socket.IO
    - `client.py`: Cliente de conexión
  - **utils/**: Utilidades comunes
- **tests/**: Pruebas unitarias
- **config/**: Configuraciones por entorno
    - `client.py`: Cliente que se conecta al servidor.
    - `socket_handlers.py`: Manejo de eventos de socket.
  - **core/**: Lógica central del juego.
    - `game_engine.py`: Motor del juego.
    - `player.py`: Clase del jugador.
    - `board.py`: Clase del tablero.
  - **utils/**: Funciones auxiliares.
    - `helpers.py`: Funciones utilizadas en diferentes partes del proyecto.

- **data/**: Archivos de datos.
  - `scores.json`: Historial de puntuaciones.
  - `config.json`: Configuración del juego.

- **tests/**: Pruebas unitarias.
  - `test_game_logic.py`: Pruebas para la lógica del juego.
  - `test_multiplayer.py`: Pruebas para la funcionalidad multijugador.

- **config/**: Configuraciones para diferentes entornos.
  - `development.py`: Configuración para desarrollo.
  - `production.py`: Configuración para producción.

- `requirements.txt`: Dependencias del proyecto.

- `setup.py`: Script de instalación del proyecto.

## Instalación
1. Clona el repositorio en tu máquina local.
2. Navega a la carpeta del proyecto.
3. Instala las dependencias utilizando el siguiente comando:
   ```
   pip install -r requirements.txt
   ```

## Uso
- Para ejecutar la versión local del juego, utiliza el siguiente comando:
  ```
  python src/local/main.py
  ```
- Para iniciar la versión web, ejecuta:
  ```
  python src/web/app.py
  ```
- Para jugar en modo multijugador, inicia el servidor y luego conecta los clientes.

## Contribuciones
Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

## Licencia
Este proyecto está bajo la Licencia MIT.