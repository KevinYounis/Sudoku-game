from __future__ import annotations
import json
from datetime import datetime, timedelta
from typing import Dict

from utils.board import Board
from player.player import Player
from utils.gamescore import GameScore
from utils.highscore_manager import HighScoreManager


def load_saves(filename: str) -> Dict[str, Dict]:
    """
    Load a json file that stores nested dictionaries.
    Returns a emtpy dictionary if the file does not exist/ invalid json.

    Args:
        filename: The name of the json file to load.

    Returns:
        A dictionary containing the nested dictionaries.

        >>> import json, tempfile, os
        >>> fd, path = tempfile.mkstemp(suffix=".json")
        >>> os.close(fd)
        >>> with open(path, "w") as f:
        ...     json.dump({"alice": {"difficulty": "easy"}}, f)
        >>> load_saves(path)["alice"]["difficulty"]
        'easy'
    """
    with open(filename, "r") as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError:
            return {}

class Game:
    """
    Orchestrate a game of Sudoku: holds the board, timing information, player reference and high score updates.
    """
    def __init__(self, player: Player, highscore_manager: HighScoreManager, difficulty: str=None) -> None:
        """
        Creates a new game session. Think about which pieces of information you need at this time
        (e.g. players, game mode, time limit, ...) and add them as arguments.
        """
        self._player: Player = player
        self._board: Board = Board(difficulty=difficulty)
        self.start_time: datetime | None = None
        self._end_time: datetime | None = None
        self._duration: timedelta = timedelta(0)
        self._is_finished: bool = False
        self.got_help: bool = False
        self._highscore_manager: HighScoreManager = highscore_manager
        
    @property
    def board(self) -> Board:
        """
        The underlying board.

        Returns:
            The underlying board.
        """
        return self._board

    @property
    def duration(self) -> timedelta:
        return self._duration

    @duration.setter
    def duration(self, duration: timedelta) -> None:
        self._duration = duration

    @property
    def start_time(self) -> datetime:
        """
        The time the game starts.

        Returns:
            The time the game starts.
        """
        return self._start_time

    @start_time.setter
    def start_time(self, value: datetime) -> None:
        """
        Sets the time the game starts.

        Args:
            value: The time the game starts.
        """
        self._start_time = value

    @property
    def end_time(self) -> datetime:
        """
        The time the game ends.

        Returns
            The time the game ends.
        """
        return self._end_time

    @property
    def is_finished(self) -> bool:
        """
        If the game is finished.

        Returns:
            True if the game is finished.
        """
        return self._is_finished

    @property
    def player(self) -> Player:
        """
        The player of the game.

        Returns:
            The player object.
        """
        return self._player

    def save_game(self, filename: str) -> None:
        """
        The method to save the game to a file. In a specified format.

        Args:
            filename: The name of the file to save the game to.

        """
        if not self.player:
            raise ValueError("Cannot save game without player")

        current_dur = self._duration
        if self.start_time and not self._is_finished:
            current_dur += datetime.now() - self.start_time

        old: Dict[str, Dict] = load_saves(filename)
        old[self.player.name] = {
            "duration": current_dur.total_seconds(),
            "is_finished": self.is_finished,
            "difficulty": self.board.difficulty,
            "board": self.board.grid
        }

        with open(filename, "w") as f:
            json.dump(old,  f, indent=4, default=str)

    @classmethod
    def load_game(cls, filename:str, player: Player, manager: HighScoreManager) -> Game:
        """
        Load a game from a file. In a specified format.

        Args:
            filename: The name of the file to load the game from.
            player: The player object that this game belongs to.
            manager: The highscore manager (instance) that this game belongs to.

        Returns:
            The loaded game, as a Game object.
        """
        with open(filename) as f:
            entries = json.load(f)
            game_object = entries[player.name]
        return Game.game_from_dict(game_object, player, manager)

    @staticmethod
    def game_from_dict(data: dict, player: Player, manager: HighScoreManager) -> Game:
        """
        Create a game from a dictionary.

        Args:
            data: The dictionary to create the game from.
            player: The player object that this game belongs to.
            manager: The highscore manager (instance) that this game belongs to.

        Returns:
            The created game, as a Game object.
        """
        val = Game(player=player, difficulty=data.get("difficulty") or "None", highscore_manager=manager)
        val.board.grid = data["board"]
        val.duration = timedelta(seconds=data.get("duration", 0))
        val._is_finished = bool(data.get("is_finished", False))
        return val

    def finish_game(self) -> None:
        """
        Clean-up code after a game session ends.
        """
        print("The Sudoku was solved")

        if self._start_time:
            self.duration += datetime.now() - self._start_time
            self._end_time = datetime.now()

        self._is_finished = True
        if self.start_time:
            if self.player:
                self.player.add_game_result(time_spent = self.duration)
                self._highscore_manager.update(GameScore(self.player.name, self.duration, self.board.difficulty, self.got_help ))


    def win_condition(self) -> bool:
        """
        What needs to be true so that a player wins?

        Returns:
            True if the game is finished, False otherwise.
        """
        if self.board and self.board.is_solved():
            return True
        return False

    def step_auto(self):
        """
        Method to solve the game automatically.
        """
        self._board.solve_game()

    def give_hint(self):
        """
        Method to get a hint for the player and set if the player received a hint.
        """
        self.got_help = self._board.give_a_hint()

    def step(self, row, col, num) -> None:
        """
        Method to make a game step that advances the gameplay

        Args:
            row: The row of the game row.
            col: The column of the game column.
            num: The number of times the player received a hint.

        """
        # If it is the first move of the player, then save the start-time
        if not self.start_time:
            self._start_time = datetime.now()
        
        # Checks, if the decision of the player is valid
        if self._board.is_valid_move(row, col, num):
            self._board.grid[row][col] = num
        else:
            print("Invalid Move!")

        # Prints the Board and lets the player choose where to put his number
        print(self._board)
        print(f"{num} was put in row {row + 1}, column {col + 1}")

        # If the step leads to solving the Sudoku, then the game is finished
        if self.win_condition():
            self._is_finished = True
            self.finish_game()


    def get_current_state(self):
        if not self.player or not self.board:
            raise ValueError(f"In {self.__class__.__name__} player or board is empty!.")

        return f"Player: {self._player.name} \n Game state: {self._is_finished} \n| Board:\n {self.board.grid}"
        

    def run(self):
        """
        Starts the game timer.
        """
        self._start_time = datetime.now()

if __name__ == '__main__':
   """
   Main Method for game module.
   """
