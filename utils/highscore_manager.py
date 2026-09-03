from __future__ import annotations

from typing import List, Optional

from utils.gamescore import GameScore

class HighScoreManager:
    def __init__(self, path: str) -> None:
        """
        This method initializes the highscore manager.

        Args:
            path (str): The path to the folder where the highscore will be stored.
        """
        self.path = path
        self._entries: List[GameScore] = []


    @property
    def entries(self) -> List[GameScore]:
        """
        Returns the list of game scores.
        Returns:
            List[GameScore]: The list of game scores.
        """
        return self._entries

    @property
    def path(self) -> str:
        """
        Returns the path to the folder where the highscore will be stored.

        Returns:
            str: The path to the folder where the highscore will be stored.
        """
        return self._path

    @path.setter
    def path(self, path: str) -> None:
        """
        Method sets the path to the folder where the highscore will be stored.
        Args:
            path (str): The path to the folder where the highscore will be stored.

        """
        self._path = path

    def load(self) -> None:
        """
            Method loads the saved highscore file.

        >>> h = HighScoreManager("nonexistent.txt")
        >>> h.load()
        >>> h.entries
        []
        """
        try:
            with open(self.path, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            self._entries = []
            return
        payload = [ln for ln in lines[1:] if ln.strip()]
        self._entries = [GameScore.from_string(entry) for entry in payload]
        for e in self._entries:
            e.convert_to_score()
        self._entries.sort(key=lambda s: s.score, reverse=True)

    def save(self) -> None:
        """
        Method saves the saved highscore file to disk.

        >>> from types import SimpleNamespace
        >>> import io
        >>> h = HighScoreManager("dummy.txt")
        >>> h._entries = [SimpleNamespace(player_name="A", score=99)]
        >>> h.path = "/tmp/testfile.txt"
        >>> h.save()
        """
        with open(self.path, "w") as f:
            f.writelines("Name:\tScore:\tTime:\tLevel:\tgot Hints:\n")
            f.writelines([f"{entry}\n" for entry in self._entries])

    def update(self, score: GameScore) -> List[GameScore]:
        """
        Method inserts score at appropriate position.

        Args:
            score: Score to insert

        Returns:
            Updated scores

        >>> from types import SimpleNamespace
        >>> h = HighScoreManager("dummy.txt")
        >>> h._entries = [SimpleNamespace(player_name="A", score=20),
        ...               SimpleNamespace(player_name="B", score=10)]
        >>> _ = h.update(SimpleNamespace(player_name="C", score=15))
        >>> [e.score for e in h._entries]
        [20, 15, 10]
        """
        i = 0
        new_val = score.convert_to_score()
        while i < len(self._entries) and self._entries[i].convert_to_score() >= new_val:
            i += 1
        self._entries.insert(i, score)
        self.save()
        return self._entries