class Player:
    def __init__(self, name: str, color: tuple[int, int, int]) -> None:
        self.name = name
        self.color = color

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)
