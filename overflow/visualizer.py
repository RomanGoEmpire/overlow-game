import pygame

from . import Grid, SQUARE_SIZE, GRID_SIZE, TOTAL_GRID_SIZE, BLOCKED_CELL

SMALLEST = 0
LARGEST = TOTAL_GRID_SIZE - 1


class Visualizer:

    def __init__(self, grid: Grid, player_colors: dict) -> None:
        self.grid = grid
        self.player_colors = player_colors

    def draw(self, screen: pygame.Surface):
        for x in range(TOTAL_GRID_SIZE):
            for y in range(TOTAL_GRID_SIZE):
                color = self.get_color(x, y)
                outline = 1
                blocked_cells_in_field = self.grid.players_with_block.values()
                if (x, y) in blocked_cells_in_field:
                    # corresponding key of the blocked cell
                    player_index = list(self.grid.players_with_block.keys())[
                        list(blocked_cells_in_field).index((x, y))
                    ]
                    color = self.player_colors[player_index]
                    # merge color with BLOCK_COLOR by using half of both colors
                    color = tuple(
                        (color[i] * 0.5 + BLOCKED_CELL * 0.5) for i in range(3)
                    )
                    outline = SQUARE_SIZE // 3

                pygame.draw.rect(
                    screen,
                    color,
                    (
                        x * SQUARE_SIZE - 1,
                        y * SQUARE_SIZE - 1,
                        SQUARE_SIZE - 1,
                        SQUARE_SIZE - 1,
                    ),
                )
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (
                        x * SQUARE_SIZE - 1,
                        y * SQUARE_SIZE - 1,
                        SQUARE_SIZE - 1,
                        SQUARE_SIZE - 1,
                    ),
                    outline,
                )

    def get_cell(self) -> tuple[int, int, str]:
        i, j = -1, -1
        action = ""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    action = "Move"
                elif event.button == 3:  # Right click
                    action = "Block"
                else:
                    action = ""
                # Get the position of the mouse
                x, y = pygame.mouse.get_pos()
                # Get the cell that was clicked
                i, j = x // SQUARE_SIZE, y // SQUARE_SIZE
                if not SMALLEST <= i <= LARGEST and SMALLEST <= j <= LARGEST:
                    return -1, -1, action
        return i, j, action

    def get_color(self, x: int, y: int):
        color_index = self.grid.get_cell(x, y)
        match color_index:
            case -1:
                return (255, 255, 255)
            case 100:
                return (0, 0, 0)  # Black
            case 101:
                return (128, 128, 128)  # Grey
            case 999:
                return (60, 60, 60)  # Dark Grey
            case 50:
                return (70, 70, 70)  # Dark Greys
            case _:
                return self.player_colors[color_index]
