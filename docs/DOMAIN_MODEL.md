# Modelo del Dominio - Tres en Raya

## Entidades Principales

### Board (Tablero)
- Representa el tablero de 3x3 del juego
- Maneja la lógica de colocación de movimientos
- Detecta condiciones de victoria y empate

### Player (Jugador)  
- Representa un jugador humano o AI
- Mantiene estadísticas y configuración
- Puede ser X u O

### GameSession (Sesión de Juego)
- Coordina una partida completa
- Mantiene el estado del juego
- Gestiona turnos de jugadores

## Casos de Uso

### StartNewGame
- Inicia una nueva partida
- Configura jugadores y tablero
- Establece estado inicial

### MakeMove
- Procesa un movimiento del jugador
- Valida el movimiento según reglas
- Actualiza estado del juego

### CheckWinner
- Verifica condiciones de victoria
- Detecta empates
- Determina el resultado final
