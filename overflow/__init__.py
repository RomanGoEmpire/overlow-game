PLAYER_COUNT = 3
GRID_SIZE = 5
TOTAL_GRID_SIZE = GRID_SIZE + 2  # ! Add two for movement tiles

SCREEN_SIZE = 800
rest = SCREEN_SIZE % GRID_SIZE
if rest != 0:
    SCREEN_SIZE -= rest
    print(f"Screen size adjusted to {SCREEN_SIZE}")
SQUARE_SIZE = SCREEN_SIZE // TOTAL_GRID_SIZE

from .player import Player
from .cell import PlayCell, MoveCell, CornerCell
from .grid import Grid
from .visualizer import Visualizer
from .game import Game
