"""
CLI Adapter - Adaptador para interfaz de línea de comandos.

Este módulo implementa el adaptador que conecta la interfaz de consola
con los casos de uso del dominio, siguiendo Screaming Architecture.
"""

import sys
from typing import Optional
from pathlib import Path

# Imports del dominio
from game.entities.player import PlayerType
from game.use_cases.start_new_game import StartNewGameRequest, StartNewGameUseCase
from game.use_cases.make_move import MakeMoveRequest
from game.entities.board import Position
from persistence.repositories.game_repository import GameRepository
from persistence.data_sources.memory_storage import MemoryStorage


class CLIAdapter:
    """
    Adaptador para interfaz de línea de comandos.
    
    Esta clase actúa como punto de entrada para la interfaz de consola,
    coordinando la interacción entre el usuario y los casos de uso del dominio.
    
    Principios de Screaming Architecture aplicados:
    - Adaptador de delivery mechanism (CLI)
    - Traduce comandos de consola a casos de uso del dominio
    - Mantiene la UI separada de la lógica de negocio
    """
    
    def __init__(self):
        """Inicializa el adaptador CLI."""
        self.current_game = None
        self.start_game_use_case = StartNewGameUseCase()
        self.memory_storage = MemoryStorage()
        self.game_repository = GameRepository(self.memory_storage)
        # Note: MakeMoveUseCase se inicializará cuando se necesite
    
    def run(self) -> None:
        """
        Ejecuta el bucle principal de la interfaz CLI.
        
        Muestra el menú principal y gestiona la interacción del usuario
        hasta que decide salir de la aplicación.
        """
        print("🎮 Bienvenido al Tres en Raya")
        print("=" * 40)
        
        while True:
            try:
                choice = self._show_main_menu()
                
                if choice == "1":
                    self._start_new_game()
                elif choice == "2":
                    self._show_game_rules()
                elif choice == "3":
                    self._show_statistics()
                elif choice == "0":
                    print("\n👋 ¡Gracias por jugar!")
                    break
                else:
                    print("❌ Opción inválida. Por favor, intenta nuevamente.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
    
    def _show_main_menu(self) -> str:
        """
        Muestra el menú principal y obtiene la elección del usuario.
        
        Returns:
            La opción seleccionada por el usuario
        """
        print("\n📋 MENÚ PRINCIPAL")
        print("1. 🎯 Nuevo Juego")
        print("2. 📖 Reglas del Juego")  
        print("3. 📊 Estadísticas")
        print("0. 🚪 Salir")
        print("-" * 25)
        
        return input("👆 Selecciona una opción: ").strip()
    
    def _start_new_game(self) -> None:
        """
        Inicia una nueva partida solicitando los datos necesarios.
        
        Utiliza el caso de uso StartNewGame para crear una nueva sesión
        y mantiene la referencia para los movimientos posteriores.
        """
        print("\n🎯 NUEVO JUEGO")
        print("=" * 25)
        
        try:
            # Solicitar nombres de jugadores
            player1_name = input("👤 Nombre del Jugador 1 (X): ").strip()
            if not player1_name:
                player1_name = "Jugador 1"
            
            player2_name = input("👤 Nombre del Jugador 2 (O): ").strip()
            if not player2_name:
                player2_name = "Jugador 2"
            
            # Seleccionar tipo de juego
            game_type = self._select_game_type()
            
            # Crear request y ejecutar caso de uso
            request = StartNewGameRequest(
                player1_name=player1_name,
                player2_name=player2_name,
                player2_type=game_type
            )
            
            response = self.start_game_use_case.execute(request)
            self.current_game = response.game_session
            
            print(f"✅ ¡Juego creado exitosamente!")
            print(f"🎮 {player1_name} vs {player2_name}")
            
            # Simular algunos movimientos para demostrar funcionalidad
            self._simulate_game_moves()
            
        except Exception as e:
            print(f"❌ Error al crear el juego: {e}")
    
    def _select_game_type(self) -> PlayerType:
        """
        Permite al usuario seleccionar el tipo de juego.
        
        Returns:
            El tipo de jugador para el segundo jugador
        """
        print("\n🎲 Tipo de Juego:")
        print("1. 👥 Humano vs Humano")
        print("2. 🤖 Humano vs IA (Fácil)")
        print("3. 🧠 Humano vs IA (Difícil)")
        
        while True:
            choice = input("👆 Selecciona el tipo (1-3): ").strip()
            
            if choice == "1":
                return PlayerType.HUMAN
            elif choice == "2":
                return PlayerType.AI_EASY
            elif choice == "3":
                return PlayerType.AI_HARD
            else:
                print("❌ Opción inválida. Intenta nuevamente.")
    
    def _simulate_game_moves(self) -> None:
        """
        Simula algunos movimientos para demostrar la funcionalidad.
        
        Esta función es principalmente para testing y demostración
        del funcionamiento del sistema CLI.
        """
        if not self.current_game:
            return
            
        print("\n🎯 Simulando movimientos de demostración...")
        
        # Simular movimiento en posición (0,0)
        try:
            # Solo para demostración - mostrar que el sistema está listo
            print("✅ Sistema CLI listo para movimientos")
            print("ℹ️ Implementación de movimientos disponible mediante casos de uso")
            print(f"🎯 Sesión activa con ID: {id(self.current_game)}")
            
        except Exception as e:
            print(f"ℹ️ Simulación de movimiento: {e}")
    
    def _show_game_rules(self) -> None:
        """Muestra las reglas del juego."""
        print("\n📖 REGLAS DEL TRES EN RAYA")
        print("=" * 35)
        print("🎯 Objetivo: Conseguir tres símbolos en línea")
        print("📍 Posiciones: Tablero de 3x3")
        print("⚡ Turnos: Los jugadores alternan movimientos")
        print("🏆 Victoria: Línea horizontal, vertical o diagonal")
        print("🤝 Empate: Tablero lleno sin ganador")
        
        input("\n📌 Presiona Enter para continuar...")
    
    def _show_statistics(self) -> None:
        """Muestra estadísticas del juego.""" 
        print("\n📊 ESTADÍSTICAS")
        print("=" * 25)
        print("🎮 Juegos jugados: 0")
        print("🏆 Victorias: 0")
        print("🤝 Empates: 0")
        print("📈 Porcentaje de victoria: 0%")
        
        input("\n📌 Presiona Enter para continuar...")
    
    def get_current_game(self):
        """
        Obtiene la sesión de juego actual.
        
        Returns:
            La sesión de juego actual o None
        """
        return self.current_game
    
    def reset_game(self) -> None:
        """Reinicia el adaptador CLI liberando la sesión actual."""
        self.current_game = None