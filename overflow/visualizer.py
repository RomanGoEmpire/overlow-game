import pygame

from . import TOTAL_GRID_SIZE, SQUARE_SIZE, Grid, PlayCell


class Visualizer:
    def __init__(self, grid: Grid):
        self.grid = grid

    def draw(self, screen):
        for x in range(TOTAL_GRID_SIZE):
            for y in range(TOTAL_GRID_SIZE):
                cell = self.grid.get_cell(x, y)
                color = cell.color
                outline = 0
                if type(cell) == PlayCell and cell.is_blocked():
                    outline = SQUARE_SIZE // 3
                    pygame.draw.rect(
                        screen,
                        cell.player.color,
                        (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                    )
                pygame.draw.rect(
                    screen,
                    color,
                    (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                    outline,
                )
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                    1,
                )

    def get_clicked_pos(self) -> tuple:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos
                x, y = x // SQUARE_SIZE, y // SQUARE_SIZE
                return x, y
        return None, None
