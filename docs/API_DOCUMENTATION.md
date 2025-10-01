# API del Juego Tres en Raya

## Endpoints Web

### POST /api/games
Crear nueva partida
```json
{
  "player1_name": "Juan",
  "player2_name": "María", 
  "player2_type": "human"
}
```

### POST /api/moves
Realizar movimiento
```json
{
  "session_id": "abc123",
  "position": {"row": 1, "col": 1}
}
```

### GET /api/games/{session_id}
Obtener estado del juego
```json
{
  "session_id": "abc123",
  "board": [["X", "", ""], ["", "O", ""], ["", "", ""]],
  "current_player": "X",
  "status": "in_progress"
}
```

## CLI Commands

- `run_cli.py` - Iniciar juego en consola
- `run_web_server.py` - Iniciar servidor web
- `run_multiplayer.py` - Iniciar servidor multiplayer
- `run_tests.py` - Ejecutar tests
