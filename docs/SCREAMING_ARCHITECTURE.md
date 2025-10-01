# Screaming Architecture - Tres en Raya

## ¿Qué es Screaming Architecture?

La Screaming Architecture es un principio donde la estructura del proyecto 
'grita' sobre qué hace la aplicación, no sobre qué frameworks utiliza.

## Aplicación en Tres en Raya

Nuestro proyecto está estructurado para que sea inmediatamente obvio 
que se trata de un juego de Tres en Raya:

- `game/` - Todo lo relacionado con el JUEGO
- `game/entities/` - Las entidades del JUEGO (Board, Player, GameSession)
- `game/use_cases/` - Los casos de uso del JUEGO (StartNewGame, MakeMove)
- `game/services/` - Los servicios del JUEGO (AIOpponent, ScoreCalculator)

La tecnología (Flask, CLI, etc.) está relegada a adaptadores.
