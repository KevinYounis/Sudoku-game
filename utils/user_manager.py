import hashlib
from datetime import timedelta
from getpass import getpass
from typing import Dict, List

from player.player import Player

class UserManager:
    def __init__(self, path: str) -> None:
        """
        Initializes user manager, to login and register new users
        """
        self.path = path
        self._entries: Dict[str, List] = {}

    @property
    def entries(self)-> Dict[str, List]:
        """
        Method returns entries of user-data.

        Returns:
            Dict[str, List] User-Data Entries

        >>> um = UserManager("dummy.txt")
        >>> um._entries = {"alice": ["hash", "10", "1"]}
        >>> um.entries["alice"][0]
        'hash'
        """
        return self._entries

    @property
    def path(self) -> str:
        """
        Method returns the path.

        Returns:
            Path method.

        >>> um = UserManager("path.txt")
        >>> um.path = "new.txt"
        >>> um.path
        'new.txt'
        """
        return self._path

    @path.setter
    def path(self, value: str) -> None:
        """
        Sets the path.
        """
        self._path = value

    def load(self) -> Dict[str, List]:
        """
        Method loads data from disk.

        Returns:
            Dict[str, List]
        """
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip().split()
                key, value = line[0], line[1:]
                self._entries[key] = value

        return self.entries

    def save(self) -> None:
        """
        Method saves data to the disk an in class specified path.
        """
        with open(self.path, "w") as f:
            for key, value in self._entries.items():
                f.write(f'{key} {" ".join(str(v) for v in value)}\n')

    def login(self) -> Player:
        """
        Method to login a player and check if the player exists.

        Returns:
            Player object
        """
        name = input("Enter username:")
        password = getpass("Enter password:")

        if name not in self._entries:
            raise ValueError("Username not found")

        hashed = hashlib.sha256(password.encode()).hexdigest()

        if hashed == self._entries[name][0]:
            print("Login successful")
            return Player(name=name, best_time=timedelta(seconds=float(self._entries[name][1])), games_played=int(self._entries[name][2]))

        raise ValueError("Password incorrect")

    def register(self) -> None:
        """
        Method to register a new user into a file.


        >>> um = UserManager("dummy.txt")
        >>> um._entries = {}
        >>> um._entries["alice"] = ["HASH", 7200.0, 0]
        >>> "alice" in um._entries
        True
        """
        usr_name = input("Please enter your username: ")

        if usr_name in self._entries:
            raise ValueError("Username already in use")

        usr_password = input("Please enter your password: ")
        usr_password_repeat = input("Please enter your password again: ")

        if usr_password != usr_password_repeat:
            raise ValueError("Passwords don't match")

        hashed = hashlib.sha256(usr_password.encode()).hexdigest()
        self._entries[usr_name] = [hashed, 7200.0, 0]

        self.save()

    def update(self, player: Player) -> None:
        """
        Method that updates the player object in a text file.

        Args:
            player (Player): The player object to update.

        >>> from types import SimpleNamespace
        >>> um = UserManager("dummy.txt")
        >>> um._entries = {"bob": ["hash", 100.0, 2]}
        >>> p = SimpleNamespace(name="bob", best_time=type("T", (), {"total_seconds": lambda self: 50.0})(), games_played=3)
        >>> um.update(p)
        >>> um._entries["bob"][1:]
        [50.0, 3]
        """
        if player.name not in self._entries:
            raise ValueError("Username not found")

        self.entries[player.name] = [self.entries[player.name][0], player.best_time.total_seconds(), player.games_played]
        self.save()
