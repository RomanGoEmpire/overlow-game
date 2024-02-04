PLAYER_COUNT = 3
GRID_SIZE = 4

SCREEN_SIZE = 500
TOTAL_GRID_SIZE = GRID_SIZE + 2
rest = SCREEN_SIZE % TOTAL_GRID_SIZE
SCREEN_SIZE -= rest
if rest != 0:
    print(
        f"Warning: Screen size was not divisible by grid size, so it was changed to {SCREEN_SIZE}"
    )
SQUARE_SIZE = SCREEN_SIZE // TOTAL_GRID_SIZE

BLOCKED_CELL = 50
BLACK_CELL = 100
MOVEMENT_CELL = 101
EDGE_CELL = 999


from .player import Player
from .grid import Grid
from .visualizer import Visualizer
from .game import Game
