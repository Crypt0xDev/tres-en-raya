class Player:
    def __init__(self, name):
        self.name = name
        self.symbol = None
        self.score = 0

    def set_symbol(self, symbol):
        self.symbol = symbol

    def increment_score(self):
        self.score += 1

    def __str__(self):
        return f"Player {self.name} with symbol {self.symbol} and score {self.score}"