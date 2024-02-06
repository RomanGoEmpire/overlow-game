import queue
import random
from typing import Any

from . import Player, Grid, Visualizer, PlayCell, MoveCell


class Game:
    def __init__(self, players: list[Player]) -> None:
        self.game_state = "SETUP"
        self.players = self.get_shuffled_players(players)
        self.next_player()
        self.grid = Grid()
        self.visualizer = Visualizer(self.grid)
        self.printed_winner = False

    def get_shuffled_players(self, players: list[Player]) -> list:
        random.shuffle(players)
        player_queue = queue.Queue()
        for player in players:
            player_queue.put(player)
        return player_queue

    def next_player(self) -> None:
        next_player = self.players.get()
        self.players.put(next_player)
        self.current_player = next_player

    def play(self) -> None:
        if self.game_state == "SETUP":
            self._setup()
        elif self.game_state == "PLAY":
            self._play()

    def _setup(self) -> None:
        if self.grid.is_setup_complete():
            self.game_state = "PLAY"
            print("Game started")
        else:
            x, y = self.visualizer.get_clicked_pos()
            if x is not None and y is not None:
                cell = self.grid._get_cell(x, y)
                if type(cell) == PlayCell and not cell.player and not cell.is_black:
                    cell.set_player(self.current_player)
                    self.next_player()

    def _play(self) -> None:
        if self.grid.is_game_over():
            self.game_state = "END"
            print(f"Game over. {self.grid.remaining_players().pop()} wins")
        else:
            x, y = self.visualizer.get_clicked_pos()
            if x is not None and y is not None:
                cell = self.grid._get_cell(x, y)
                if type(cell) == MoveCell and not cell.is_blocked:
                    self.grid.move(x, y)
                    self.update_players()
                    self.grid.update_blocked_cells()
                elif type(cell) == PlayCell and cell.is_black and not cell.player:
                    self.grid.block(x, y, self.current_player)
                    self.update_players()
                    self.grid.update_blocked_cells()

    def update_players(self) -> None:
        remaining_players = self.grid.remaining_players()
        diff = [
            player for player in self.players.queue if player not in remaining_players
        ]
        for player in diff:
            print(f"Player {player} is out")
            self.players.queue.remove(player)
            self.grid.remove_blocked_cells(player)
            self.grid.update_blocked_cells()
        self.next_player()
