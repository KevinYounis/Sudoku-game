import random

class Board:
        
        def __init__(self, difficulty = "easy"):
                ''' 
                Constructor of Board.
                Stores the grid for the Sudoku and the difficulty
                '''
                self._difficulty = difficulty

                self._grid = []
                for i in range(9):
                        row = [0] * 9
                        self._grid.append(row)

                self.fill_board()

                self.remove_numbers(self._difficulty)
                
        @property
        def difficulty(self):
                ''' Getter for difficulty '''

                return self._difficulty
        
        @property
        def grid(self):
                ''' Getter for grid '''
                return self._grid
        
        @grid.setter
        def grid(self, new_grid):
                ''' Setter for grid '''
                if isinstance(new_grid, list) and len(new_grid) == 9:
                        self._grid = new_grid
                else:
                        raise ValueError("Grid must be a 9x9 list of lists.")
        
        def is_valid_move(self, row, col, num, check_solvable=True):
                """
                Checks if placing num in the selected field is valid.

                >>> b = Board("really easy")
                >>> b.grid = [[0]*9 for _ in range(9)]
                >>> b.is_valid_move(0, 0, 5)
                True
                >>> b.grid[0][0] = 5
                >>> b.is_valid_move(0, 1, 5)
                False
                """
                
                # Check, if field is empty
                if self.grid[row][col] != 0:
                        return False
                
                # Check, if number is in the row
                if num in self.grid[row]:
                        return False
                
                # Check, if number is in the column
                for r in range(9):
                        if self.grid[r][col] == num:
                                return False
                
                # Check, if number is in the 3x3 sub-grid
                start_row = (row // 3) * 3
                start_col = (col // 3) * 3

                for r in range(start_row, start_row + 3):
                        for c in range(start_col, start_col + 3):
                                if self.grid[r][c] == num:
                                        return False

                 # Optional: Check if the Sudoku is still solvable with this number
                if check_solvable:               
                        # Copy of the current grid to test, if solvable
                        temp_grid = [row[:] for row in self.grid]
                        temp_grid[row][col] = num

                        # Create a temporary Board object for testing
                        temp_board = Board()
                        temp_board.grid = temp_grid

                        # Check if Sudoku is still solvable with this number
                        if not temp_board.has_solution():
                                return False
                
                return True
        
        def has_solution(self):
                '''
                Checks if the current Sudoku grid still has a valid solution by using recursion and backtracking, similar to fill_board().
                
                >>> b = Board("really easy")
                >>> b.grid = [[0]*9 for _ in range(9)]  # Empty Sudoku
                >>> b.has_solution()
                True
                >>> b.grid[0][0] = 5
                >>> b.grid[0][1] = 5 # invalid move
                >>> b.has_solution()
                False
                '''
                
                for row in range(9):
                        for col in range(9):
                                if self.grid[row][col] == 0:
                                        for num in range(1, 10):
                                                # Similiar to fill.board()
                                                if self.is_valid_move(row, col, num, check_solvable=False):
                                                        self.grid[row][col] = num
                                                        if self.has_solution():
                                                                return True
                                                        self.grid[row][col] = 0
                                        return False
                return True
        
        def fill_board(self):
                '''
                Fills the empty board with valid numbers.

                >>> b = Board("really easy")
                >>> b.grid = [[0]*9 for _ in range(9)]
                >>> b.fill_board()
                True
                '''

                # All possible inputs 
                numbers = list(range(1, 10))

                # Iterate through all fields
                for row in range(9):
                        for col in range(9):
                                if self.grid[row][col] == 0:
                                        # For every loop, randomize the list of numbers
                                        random.shuffle(numbers)
                                        for num in numbers:
                                                if self.is_valid_move(row, col, num, check_solvable=False):
                                                        self.grid[row][col] = num
                                                        # Recursion
                                                        if self.fill_board():
                                                                return True
                                                        # Backtracking until we get to the source of the mistake
                                                        self.grid[row][col] = 0
                                        return False
                return True
        
        def remove_numbers(self, difficulty = "easy"):
                '''
                Removes numbers from the board based on difficulty.

                >>> b = Board("really easy")
                >>> before = sum(1 for row in b.grid for c in row if c != 0)
                >>> b.remove_numbers("hard")
                >>> after = sum(1 for row in b.grid for c in row if c != 0)
                >>> after <= before
                True
                '''
                
                # The game difficulty decides, how many numbers will be left in the Sudoku

                max_subtract = 0
                if difficulty == "really easy":
                        max_subtract = 25
                if difficulty == "easy":
                        max_subtract = 35
                if difficulty == "medium":
                        max_subtract = 45
                if difficulty == "hard":
                        max_subtract = 55

                count = 0

                # Here, we choose a random field
                while count < max_subtract:
                        row = random.randint(0, 8)
                        col = random.randint(0, 8)

                        # Now we delete the number in the selected field
                        if self.grid[row][col] != 0:
                                self.grid[row][col] = 0
                                count += 1



        
        def is_solved(self):
                '''
                Checks if the Sudoku is correctly solved.

                >>> b = Board("really easy")
                >>> b.solve_game()
                >>> b.is_solved()
                True
                >>> b.grid[0][0] = 0
                >>> b.is_solved()
                False
                '''

                # Check, if the whole board was filled
                for row in range(9):
                        for col in range(9):
                                if  self.grid[row][col] == 0:
                                        return False
                
                # Check for every number, if the move is valid
                for row in range(9):
                        for col in range(9):
                                # Save the number
                                number = self.grid[row][col]

                                # Make the number temporarly invalid
                                self.grid[row][col] = 0
                                # Check, if the number is a valid move
                                if not self.is_valid_move(row, col, number, check_solvable= False):
                                        # Put the number in the board again
                                        self.grid[row][col] = number
                                        return False
                                
                                # Put the number in the board again
                                self.grid[row][col] = number
                return True
        
        
        def solve_game(self):
                '''
                Solves the Sudoku board by filling it with a valid solution.

                >>> b = Board("hard")
                >>> b.solve_game()
                >>> b.is_solved()
                True
                '''

                # Solve the Sudoku by filling it with valid numbers
                self.fill_board()

        def give_a_hint(self):
                """
                Gives a safe hint by revealing one valid number that does not make the Sudoku unsolvable.

                >>> b = Board("easy")
                >>> before = str(b)
                >>> b.give_a_hint()
                Hint given in row ...
                True
                >>> after = str(b)
                >>> before == after
                False
                """

                # Copy of the original grid
                copy_original_grid = [row[:] for row in self.grid]

                # all possible empty spots
                empty_spots = [(r, c) for r in range(9) for c in range(9) if self.grid[r][c] == 0]

                random.shuffle(empty_spots)  # We try different spots

                for (row, col) in empty_spots:
                        # Test all possible numbers in this spot
                        numbers = list(range(1, 10))
                        random.shuffle(numbers)
                        for num in numbers:
                                if self.is_valid_move(row, col, num, check_solvable=False):
                                        # Set the number temporarly
                                        self.grid[row][col] = num

                                        # Test, if the Sudoku is solvable
                                        test_board = Board(self.difficulty)
                                        test_board.grid = [row[:] for row in self.grid]

                                        if test_board.fill_board():
                                                print(f"Hint given in row {row + 1}, column {col + 1}: {num}")
                                                return True  # Succesful and save hint

                                        # Delete the hint, if unsolvable
                                        self.grid[row][col] = 0

                # If no save hint was found, restore the original board
                self.grid = copy_original_grid
                print("No safe hint could be given.")
                return False


        def __str__(self):
                '''returns the current grid of the Sudoku as a string, with row and column labels'''
                
                result = "    1 2 3   4 5 6   7 8 9\n"  # Column labels
                result += "  +-------+-------+-------+\n" # first horizontal seperation
                for i in range(9):
                        result += f"{i+1} | "  # Row label
                        for j in range(9):
                                number = self.grid[i][j]
                                if number != 0:
                                        result += str(number)
                                else:
                                        result += "." # Stands for empty spots
                                result += " "
                                if (j + 1) % 3 == 0:
                                        result += "| " # vertical seperations
                        result += "\n"
                        if (i + 1) % 3 == 0:
                                result += "  +-------+-------+-------+\n" # horizontal seperations
                return result

        

if __name__ == '__main__':

        # Create a Sudoku
        b = Board("hard")
        print(b)

        # give multiple hints
        i = 0
        while i < 10:
                b.give_a_hint()
                i += 1
        
        print(b)

        # Solve the Sudoku
        b.solve_game()
        print(b)
        