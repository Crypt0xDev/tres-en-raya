class ConsoleUI:
    def display_welcome(self):
        print("¡Bienvenido al juego Tres en Raya!")
    
    def display_board(self, board):
        for row in board:
            print(" | ".join(row))
            print("-" * 9)
    
    def get_player_input(self, player):
        while True:
            try:
                move = int(input(f"{player}, ingresa tu movimiento (1-9): ")) - 1
                if move < 0 or move > 8:
                    raise ValueError
                return move
            except ValueError:
                print("Entrada no válida. Por favor, ingresa un número entre 1 y 9.")
    
    def display_winner(self, player):
        print(f"¡Felicidades {player}, has ganado!")
    
    def display_draw(self):
        print("¡Es un empate!")