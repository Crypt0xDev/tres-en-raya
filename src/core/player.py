from typing import Optional


class Player:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.symbol: Optional[str] = None
        self.score: int = 0

    def set_symbol(self, symbol: str) -> None:
        self.symbol = symbol

    def increment_score(self) -> None:
        self.score += 1

    def __str__(self) -> str:
        return f"Player {self.name} with symbol {self.symbol} and score {self.score}"
