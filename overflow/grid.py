from random import randint
from . import (
    GRID_SIZE,
    PLAYER_COUNT,
    TOTAL_GRID_SIZE,
    BLACK_CELL,
    BLOCKED_CELL,
    EDGE_CELL,
    MOVEMENT_CELL,
)


class Grid:
    def __init__(self) -> None:
        self.grid = self.initialize()
        self.last_move = None
        self.players_with_block = {}

    def winner(self) -> int:
        # merge 2D list into 1D list
        colors = [color for row in self.grid for color in row]
        colors = set(colors)
        colors.discard(BLACK_CELL)
        colors.discard(BLOCKED_CELL)
        colors.discard(EDGE_CELL)
        colors.discard(MOVEMENT_CELL)
        if len(colors) == 1:
            return colors.pop()
        return None

    def get_grid(self) -> list[list[int]]:
        return self.grid

    def get_row(self, row: int) -> list[int]:
        return self.grid[row]

    def get_column(self, column: int) -> list[int]:
        return [self.grid[i][column] for i in range(TOTAL_GRID_SIZE)]

    def set_cell(self, x: int, y: int, value: int) -> None:
        self.grid[x][y] = value

    def get_cell(self, x: int, y: int) -> int:
        return self.grid[x][y]

    def get_opposite_cell(self, x: int, y: int) -> int:
        if x == 0:
            return GRID_SIZE + 1, y
        elif x == GRID_SIZE + 1:
            return 0, y
        elif y == 0:
            return x, GRID_SIZE + 1
        elif y == GRID_SIZE + 1:
            return x, 0
        else:
            raise ValueError("Invalid movement cell")

    def move(self, x: int, y: int) -> None:
        if y == 0:
            row = self.get_row(x)
            row = [MOVEMENT_CELL, BLACK_CELL] + row[1:-2] + [MOVEMENT_CELL]
            self.grid[x] = row
        elif y == GRID_SIZE + 1:
            row = self.get_row(x)
            row = [MOVEMENT_CELL] + row[2:-1] + [BLACK_CELL, MOVEMENT_CELL]
            self.grid[x] = row
        elif x == 0:
            column = self.get_column(y)
            column = [MOVEMENT_CELL, BLACK_CELL] + column[1:-2] + [MOVEMENT_CELL]
            for i in range(TOTAL_GRID_SIZE):
                self.grid[i][y] = column[i]
        elif x == GRID_SIZE + 1:
            column = self.get_column(y)
            column = [MOVEMENT_CELL] + column[2:-1] + [BLACK_CELL, MOVEMENT_CELL]
            for i in range(TOTAL_GRID_SIZE):
                self.grid[i][y] = column[i]
        else:
            raise ValueError("Invalid movement cell")
        # get the opposite cell and set it to BLOCKED_CELL
        oppsite_x, oppsite_y = self.get_opposite_cell(x, y)
        self.grid[oppsite_x][oppsite_y] = BLOCKED_CELL
        self.last_move = (oppsite_x, oppsite_y)

    def unblock(self, x: int, y: int) -> None:

        self.set_cell(x, y, BLACK_CELL)
        self.set_cell(0, y, MOVEMENT_CELL)
        self.set_cell(GRID_SIZE + 1, y, MOVEMENT_CELL)
        self.set_cell(x, 0, MOVEMENT_CELL)
        self.set_cell(x, GRID_SIZE + 1, MOVEMENT_CELL)

    def block(self, x: int, y: int, player_number: int) -> None:
        current_block = self.players_with_block.get(player_number)
        if self.get_cell(x, y) == BLACK_CELL:
            self.players_with_block[player_number] = (x, y)
            # remove the current block from the grid
            if current_block:
                self.unblock(*current_block)

    def initialize(self) -> None:
        total_cells = GRID_SIZE * GRID_SIZE
        black_cells = total_cells % PLAYER_COUNT
        # * 2 to add the border cells
        grid = [[-1 for _ in range(TOTAL_GRID_SIZE)] for _ in range(TOTAL_GRID_SIZE)]
        # Set the border cells to MOVEMENT_CELL
        grid[0] = [MOVEMENT_CELL for _ in range(TOTAL_GRID_SIZE)]
        grid[-1] = [MOVEMENT_CELL for _ in range(TOTAL_GRID_SIZE)]
        for i in range(TOTAL_GRID_SIZE):
            grid[i][0] = MOVEMENT_CELL
            grid[i][-1] = MOVEMENT_CELL
        # Set the edge cells to EDGE_CELL
        grid[0][0] = EDGE_CELL
        grid[0][-1] = EDGE_CELL
        grid[-1][0] = EDGE_CELL
        grid[-1][-1] = EDGE_CELL

        # Get the (x,y) coordinates of the black cells in the grid randomly
        for _ in range(black_cells):
            x, y = -1, -1
            while x == -1 and y == -1 or grid[x][y] == BLACK_CELL:
                x, y = randint(1, GRID_SIZE - 2), randint(1, GRID_SIZE - 2)
            grid[x][y] = BLACK_CELL
        return grid

    def is_full(self) -> bool:
        return not any(-1 in row for row in self.grid)

    def is_empty(self, x: int, y: int) -> bool:
        return self.grid[x][y] == -1

    def valid_placement_cell(self, x: int, y: int):
        return (
            1 <= x <= GRID_SIZE
            and 1 <= y <= GRID_SIZE
            and self.get_cell(x, y) != BLACK_CELL
            and self.is_empty(x, y)
        )

    def valid_blocking_cell(self, x: int, y: int):
        return (
            1 <= x <= GRID_SIZE
            and 1 <= y <= GRID_SIZE
            and self.get_cell(x, y) == BLACK_CELL
        )

    def valid_movement_cell(self, x: int, y: int):
        is_edge = x == 0 or x == GRID_SIZE + 1 or y == 0 or y == GRID_SIZE + 1
        is_corner = (x == 0 or x == GRID_SIZE + 1) and (y == 0 or y == GRID_SIZE + 1)
        return is_edge and not is_corner and self.get_cell(x, y) != BLOCKED_CELL

    def update_blocked_cells(self):
        xs = set()
        ys = set()
        for _, (x, y) in list(self.players_with_block.items()):
            xs.add(x)
            ys.add(y)
            self.set_cell(x, y, BLOCKED_CELL)
        for x in xs:
            self.set_cell(x, 0, BLOCKED_CELL)
            self.set_cell(x, GRID_SIZE + 1, BLOCKED_CELL)
        for y in ys:
            self.set_cell(0, y, BLOCKED_CELL)
            self.set_cell(GRID_SIZE + 1, y, BLOCKED_CELL)
        if self.last_move:
            x, y = self.last_move
            self.set_cell(x, y, BLOCKED_CELL)
            self.last_move = None

    def is_on_board(self, player_index: int) -> bool:
        for x in range(TOTAL_GRID_SIZE):
            for y in range(TOTAL_GRID_SIZE):
                if self.get_cell(x, y) == player_index:
                    return True
        return False
