from .player import Player
from .grid import Grid
from .visualizer import Visualizer

GAME_STATE = ["SETUP", "GAME", "END"]


class Game:
    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.give_players_index()
        self.grid = Grid()
        # create a dictionary of player index to player color
        self.visualizer = Visualizer(self.grid, self._get_player_colors())
        self.current_player = 0
        self.game_state = GAME_STATE[0]
        self.printed = False

    def _get_player_colors(self):
        return {self.players.index(player): player.color for player in self.players}

    def next_player(self):
        active_players = [player for player in self.players if player.in_game]
        self.current_player = (self.current_player + 1) % len(active_players)
        self.printed = False

    def play(self):
        if not self.printed:
            print(f"Player {self.current_player + 1}'s turn")
            self.printed = True
        if self.game_state == GAME_STATE[0]:
            self._setup()
        elif self.game_state == GAME_STATE[1]:
            self._game()

    def _setup(self):
        if self.grid.is_full():
            print("Game setup complete")
            self.game_state = GAME_STATE[1]
            print("Game started")
        else:
            i, j, _ = self.visualizer.get_cell()
            # only update the player if the selected cell is empty
            if self.grid.valid_placement_cell(i, j):
                self.grid.set_cell(i, j, self.current_player)
                self.next_player()

    def _game(self):
        if self.grid.winner():
            print("Game over")
            print(f"Player {self.current_player + 1} wins!")
            self.game_state = GAME_STATE[2]
        else:
            i, j, move_or_block = self.visualizer.get_cell()
            if move_or_block == "Move" and self.grid.valid_movement_cell(i, j):
                self.grid.move(i, j)
                self.update_active_players()
                self.grid.update_blocked_cells()
                self.next_player()
            elif move_or_block == "Block" and self.grid.valid_blocking_cell(i, j):
                self.grid.block(i, j, self.current_player)
                self.update_active_players()
                self.grid.update_blocked_cells()
                self.next_player()

    def update_active_players(self):
        for player in self.players:
            index = player.index
            if not self.grid.is_on_board(index):
                player.in_game = False
                print(f"Player {index} is out of the game")
                if index in self.grid.players_with_block.keys():
                    current_block = self.grid.players_with_block.pop(index)
                    self.grid.unblock(*current_block)

    def give_players_index(self):
        for index, player in enumerate(self.players):
            player.index = index
