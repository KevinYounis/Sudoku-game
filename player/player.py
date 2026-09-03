######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# FAI Universität Augsburg           #
# WiSe 2025/26                       #
# Software Assignment                #
######################################
from datetime import timedelta


class Player:

    def __init__(self, name, best_time: timedelta = None, games_played: int = 0):
        '''
        Creates a new Player. 
        Stores their name, best time, and number of games played.
        '''
        self._name = name
        self._best_time = best_time
        self._games_played = games_played

    @property
    def name(self):
        ''' Getter for name '''
        return self._name
    
    @property
    def best_time(self):
        ''' Getter for best_time '''
        return self._best_time
    
    @best_time.setter
    def best_time(self, new_best_time):
            ''' Setter for best_time '''
            if isinstance(new_best_time, timedelta) and new_best_time < self._best_time:
                    self._best_time = new_best_time
            else:
                    raise ValueError("New best time must be of type timedelta and better then current best time.")
    
    @property
    def games_played(self):
        ''' Getter for games_played '''
        return self._games_played
    
    def add_game_result(self, time_spent):
        '''
        Updates the stats of the player after finishing a game.

        - Increments the `games_played` counter.
        - Updates the best time if the new time is better.

        >>> from datetime import timedelta
        >>> p = Player("Mario")
        >>> p.add_game_result(timedelta(minutes=5))
        >>> p.games_played
        1
        >>> p.best_time == timedelta(minutes=5)
        True
        >>> p.add_game_result(timedelta(minutes=3))
        >>> p.best_time == timedelta(minutes=3)
        True
        '''

        # Counter for how many games the player finished
        self._games_played += 1

        # If the new time spent for the Sudoku is better than the current "best-time", then it will be saved as such
        if not time_spent == None:
            if self._best_time is None or time_spent < self._best_time:
                self._best_time = time_spent

    def __str__(self):
        ''' Returns the infos of the player (name, games played, best time) '''
        
        return f"Player: {self._name}, {self._games_played} games, Best Time: {self._best_time}" 


if __name__ == '__main__':
    '''
    write additional testing code here for things that don't work well as unit tests:
    '''
    player1 = Player('Yoshi')  # create new player
    player2 = Player('Peach')  # create new player
