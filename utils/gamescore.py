from __future__ import annotations
from datetime import timedelta


class GameScore:
    _time_limit = 7200
    _score_limit = 1000

    def __init__(self, player_name: str, game_time: timedelta = None, level: str = "", help: bool = False) -> None:
        """
        Initialize a game score object. This holds information about the game score and
        the player

        >>> from datetime import timedelta
        >>> g = GameScore("Alice", timedelta(seconds=60))
        >>> g.player_name
        'Alice'
        >>> g.game_time.total_seconds()
        60.0
        """
        self._player_name = player_name
        self._score = 0
        self.game_time = game_time
        self.level = level
        self.help = help

    @property
    def player_name(self) -> str:
        """
        Return the player's name

        Returns:
            str: the player's name
        """
        return self._player_name

    @property
    def score(self)-> int:
        """
        Returns the score of the game score

        Returns:
            int: the score of the game score
        """
        return self._score

    @property
    def game_time(self)->timedelta:
        """
        Returns the game time of the game score

        Returns:
            timedelta: the game time of the game score
        """
        return self._game_time

    @game_time.setter
    def game_time(self, value: timedelta) -> None:
        """
        Sets the game time of the game score
        """
        self._game_time = value

    @property
    def level(self)-> str:
        """
        Returns the level of the game score

        Returns:
             str: the level of the game score
        """
        return self._level

    @level.setter
    def level(self, value: str):
        """
        Sets the level of the game score

        Args:
            value (str): the level of the game score
        """
        self._level = value

    @property
    def help(self) -> bool:
        """
        Returns whether the player got help during the game

        Returns:
            bool: whether the player got help during the game
        """
        return self._help

    @help.setter
    def help(self, value: bool) -> None:
        """
        Sets the if the player got help during the game

        Args:
            value (bool): whether the player got help during the game
        """
        self._help = value

    def convert_to_score(self) -> int:
        """
        Simple math-formula to convert the time to a score

        Returns:
            int: the score of the game score

        >>> from datetime import timedelta
        >>> g = GameScore("Bob", timedelta(seconds=0))
        >>> g.convert_to_score() > 0
        True
        >>> g = GameScore("Bob", timedelta(seconds=8000))  # über Limit
        >>> g.convert_to_score()
        0
        """
        if self.game_time.total_seconds() > self._time_limit:
            return 0

        self._score = (GameScore._score_limit * (GameScore._time_limit - self.game_time.total_seconds()) ** 3) / GameScore._time_limit ** 3

        return int(self.score)

    def __str__(self) -> str:
        """
        Returns a string representation of the game score

        Returns:
            str: the string representation of the game score
        """
        return f"{self.player_name}\t{self.convert_to_score()}\t{self.game_time.total_seconds()}\t{self.level}\t{self.help}"

    def __repr__(self) -> str:
        """
        Returns a string representation of the game score

        Returns:
            str: the string representation of the game score
        """
        return self.__str__()

    @staticmethod
    def from_string(s: str) -> GameScore:
        """
        Method to convert a string representation of the game score into a GameScore object

        Args:
            s (str): the string representation of the game score

        Returns:
            GameScore: the game score object
        """
        parts = s.strip().split("\t")

        return GameScore(
            player_name=parts[0],
            game_time=timedelta(seconds=float(parts[2])),
            level=None if parts[3].strip() in ("", "None") else parts[3].strip(),
            help=(parts[4] == "True")
        )