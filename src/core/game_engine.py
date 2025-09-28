class GameEngine:
    def __init__(self):
        self.games = {}
        self.game_counter = 0

    def start_game(self, player1_name=None, player2_name=None):
        from .board import Board
        from .player import Player

        self.game_counter += 1
        game_id = str(self.game_counter)

        player1 = Player(name=player1_name or "Player 1")
        player2 = Player(name=player2_name or "Player 2")
        player1.set_symbol("X")
        player2.set_symbol("O")

        self.games[game_id] = {
            "board": Board(),
            "players": [player1, player2],
            "current_turn": 0,
            "status": "active",
            "winner": None,
        }

        return game_id

    def get_game_status(self, game_id):
        if game_id not in self.games:
            return {"error": "Game not found"}

        game = self.games[game_id]
        return {
            "status": game["status"],
            "board": game["board"].board,
            "current_player": game["players"][game["current_turn"]].name,
            "winner": game["winner"],
        }

    def make_move(self, game_id, player_name, position):
        if game_id not in self.games:
            return {"error": "Game not found"}

        game = self.games[game_id]
        if game["status"] != "active":
            return {"error": "Game is not active"}

        current_player = game["players"][game["current_turn"]]
        if current_player.name != player_name:
            return {"error": "Not your turn"}

        # Convert position to row, col
        row, col = divmod(position, 3)

        if game["board"].make_move(row, col):
            winner = game["board"].check_winner()
            if winner:
                game["status"] = "finished"
                game["winner"] = winner
                return {"success": True, "winner": winner}
            elif game["board"].is_board_full():
                game["status"] = "finished"
                game["winner"] = "draw"
                return {"success": True, "winner": "draw"}
            else:
                game["current_turn"] = (game["current_turn"] + 1) % 2
                return {"success": True}
        else:
            return {"error": "Invalid move"}

    def end_game(self, game_id):
        if game_id in self.games:
            del self.games[game_id]
            return {"success": True}
        return {"error": "Game not found"}
