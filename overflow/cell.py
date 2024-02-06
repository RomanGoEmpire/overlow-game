WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (125, 125, 125)
DARK_GREY = (50, 50, 50)


class Cell:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.color = WHITE

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.color})"

    def __repr__(self) -> str:
        return str(self)


class PlayCell(Cell):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.player = None
        self.color = WHITE
        self.is_black = False

    def is_blocked(self) -> bool:
        return self.is_black and self.player

    def block_by_player(self, player) -> None:
        self.player = player
        self.color = GREY

    def set_black(self) -> None:
        self.player = None
        self.color = BLACK
        self.is_black = True

    def set_player(self, player) -> None:
        self.player = player
        self.color = player.color

    def update_position(self, x, y) -> None:
        self.x = x
        self.y = y


class MoveCell(Cell):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.color = GREY
        self.is_blocked = False

    def block(self) -> None:
        self.is_blocked = True
        self.color = DARK_GREY

    def unblock(self) -> None:
        self.is_blocked = False
        self.color = GREY


class CornerCell(Cell):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.color = DARK_GREY

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.color})"

    def __repr__(self) -> str:
        return str(self)
