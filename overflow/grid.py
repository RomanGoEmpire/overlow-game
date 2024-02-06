from . import GRID_SIZE, PLAYER_COUNT, TOTAL_GRID_SIZE, PlayCell, MoveCell, CornerCell


class Grid:
    def __init__(self) -> None:
        self.grid = self._create_grid()
        self._initialize_black_cells()
        self.last_block = None

    def _create_grid(self) -> list[list]:

        # corner cells
        corner_cells = [
            CornerCell(0, 0),
            CornerCell(0, TOTAL_GRID_SIZE - 1),
            CornerCell(TOTAL_GRID_SIZE - 1, 0),
            CornerCell(TOTAL_GRID_SIZE - 1, TOTAL_GRID_SIZE - 1),
        ]

        # outer ring of the grid is for movement cells
        upper_movement_cells = [MoveCell(i, 0) for i in range(1, TOTAL_GRID_SIZE - 1)]
        lower_movement_cells = [
            MoveCell(i, TOTAL_GRID_SIZE - 1) for i in range(1, TOTAL_GRID_SIZE - 1)
        ]
        left_movement_cells = [MoveCell(0, i) for i in range(1, TOTAL_GRID_SIZE - 1)]
        right_movement_cells = [
            MoveCell(TOTAL_GRID_SIZE - 1, i) for i in range(1, TOTAL_GRID_SIZE - 1)
        ]
        grid = (
            corner_cells
            + upper_movement_cells
            + lower_movement_cells
            + left_movement_cells
            + right_movement_cells
        )
        # inner grid is for play cells
        for i in range(1, TOTAL_GRID_SIZE - 1):
            row = [PlayCell(i, j) for j in range(1, TOTAL_GRID_SIZE - 1)]
            grid.extend(row)

        # sort by x and y
        grid = sorted(grid, key=lambda cell: (cell.x, cell.y))
        return grid

    def _initialize_black_cells(self) -> None:
        total_cels = GRID_SIZE**2

        rest = total_cels % PLAYER_COUNT
        if rest == 1:
            if GRID_SIZE % 2 == 1:
                # add a black cell in the middle
                middle = TOTAL_GRID_SIZE // 2
                self._get_cell(middle, middle).set_black()
            else:
                # add black cells to each corner
                self._get_cell(1, 1).set_black()
                self._get_cell(1, TOTAL_GRID_SIZE - 2).set_black()
                self._get_cell(TOTAL_GRID_SIZE - 2, 1).set_black()
                self._get_cell(TOTAL_GRID_SIZE - 2, TOTAL_GRID_SIZE - 2).set_black()

    def _play_cells(self) -> list[PlayCell]:
        return [cell for cell in self.grid if isinstance(cell, PlayCell)]

    def _move_cells(self) -> list[MoveCell]:
        return [cell for cell in self.grid if isinstance(cell, MoveCell)]

    def is_game_over(self) -> bool:
        # get set of all players
        player_cells = self._play_cells()
        players = self.remaining_players()
        # if there is only one player left
        return len(players) == 1

    def remaining_players(self) -> set:
        player_cells = self._play_cells()
        return {
            cell.player for cell in player_cells if cell.player and not cell.is_black
        }

    def is_setup_complete(self) -> bool:
        # get set of all players
        player_cells = self._play_cells()
        empty_cells = [
            cell for cell in player_cells if not cell.player and not cell.is_black
        ]
        return not empty_cells

    def _get_cell(self, x, y) -> PlayCell | MoveCell:
        # filter the cell with x and y
        cell = next((cell for cell in self.grid if cell.x == x and cell.y == y), None)
        return cell

    def move(self, x, y) -> None:
        self._block_last_move(x, y)
        player_cells = self._play_cells()
        direction = self._get_direction(x, y)
        # Get the row or column of the cells
        if direction in ["UP", "DOWN"]:
            cells = [cell for cell in player_cells if cell.x == x]
        else:
            cells = [cell for cell in player_cells if cell.y == y]
        # sort the cells
        if direction == "UP" or direction == "LEFT":
            cells = sorted(cells, key=lambda cell: (cell.x, cell.y), reverse=True)
        else:
            cells = sorted(cells, key=lambda cell: (cell.x, cell.y))
        # save the positions of the cells to have them for the new cells
        positions = [(cell.x, cell.y) for cell in cells]
        removed_cell = cells[-1]
        # create a new cell
        new_cell = PlayCell(removed_cell.x, removed_cell.y)
        new_cell.set_black()

        new_cells = [new_cell] + cells[:-1]
        for i, cell in enumerate(new_cells):
            cell.x, cell.y = positions[i]

        # remove the old cell and add the new cell
        for cell in cells:
            self.grid.remove(cell)
        self.grid += new_cells

    def _get_direction(self, x, y) -> str:
        # get the direction of the move
        if y == 0:
            return "DOWN"
        if y == TOTAL_GRID_SIZE - 1:
            return "UP"
        if x == 0:
            return "RIGHT"
        if x == TOTAL_GRID_SIZE - 1:
            return "LEFT"

    def _block_last_move(self, x, y) -> None:
        self._unblock_last_move()
        if x == 0:
            self.last_block = (TOTAL_GRID_SIZE - 1, y)
        elif x == TOTAL_GRID_SIZE - 1:
            self.last_block = (0, y)
        elif y == 0:
            self.last_block = (x, TOTAL_GRID_SIZE - 1)
        else:
            self.last_block = (x, 0)

    def _unblock_last_move(self) -> None:
        if self.last_block:
            self._get_cell(*self.last_block).unblock()
            self.last_block = None

    def block(self, x, y, player) -> None:
        # remove last block of the player
        self.remove_blocked_cells(player)
        # block the cell
        cell = self._get_cell(x, y)
        cell.update_to_blocker(player)
        # update the blocked cells
        self._unblock_last_move()
        self.update_blocked_cells()

    def update_blocked_cells(self) -> None:
        x_blocked = set()
        y_blocked = set()
        for cell in self._play_cells():
            if cell.is_blocked():
                x_blocked.add(cell.x)
                y_blocked.add(cell.y)

        for cell in self._move_cells():
            if (
                cell.x in x_blocked
                or cell.y in y_blocked
                or self.last_block == (cell.x, cell.y)
            ):
                cell.block()
            else:
                cell.unblock()

    def remove_blocked_cells(self, player) -> None:
        for cell in self._play_cells():
            if cell.is_blocked() and cell.player == player:
                cell.set_black()
