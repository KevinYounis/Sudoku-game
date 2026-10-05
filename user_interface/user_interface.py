import sys
import os
from game.game import Game

class UI:
    '''
    Class for any inputs and outputs.

    '''

    def __init__(self, user_manager, highscore_manager, save_path):
        '''
        Constructor of the UI. Mainly assigns values to attributes that are used for file handling.
        '''
        self._save_path = save_path
        self._user_manager = user_manager
        self._highscore_manager = highscore_manager
        self._is_saved = False

    @property
    def is_saved(self) -> bool:
        return self._is_saved

    @is_saved.setter
    def is_saved(self, value: bool):
        self._is_saved = value

    
    def playing_input(self, playing_game):
        """
        Handles the gameplay interactions with the user.
        """
        while True:
            # We enter the loop and expect the player to choose one of the four options. 
            # If the player inputs something invalid, we go to the next iteration of the loop.

            print("1) Play")
            print("2) Get a hint")
            print("3) See the solution")
            print("4) Save game")

            play = input("Select an option: ").strip().lower()

            if play == "1":
                while True:
                    # This loop handles invalid moves

                    while True:
                        # This loop specifically handles incorrect input when filling a square.

                        row = int(input("Enter row: "))
                        col = int(input("Enter column: "))
                        num = int(input("Enter number: "))
                        if not (1 <= row <= 9 and 1 <= col <= 9 and 1 <= num <= 9):
                            print("Please only input numbers from 1-9.")
                            continue    # Ask the user again for the input

                        break   # Only exit the loop if the input was valid

                    row -= 1
                    col -= 1 

                    if playing_game._board.is_valid_move(row, col, num):
                        os.system('cls' if os.name == 'nt' else 'clear')
                        playing_game.step(row, col, num)
                        break  # gültiger Zug, Schleife verlassen
                    else:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        playing_game.step(row, col, num)
                        break  # erneut eingeben

                # Check after every play whether the game is solved and then saves game and score
                if playing_game.win_condition():
                    break
                  

            elif play == "2":
                # If the player requests it, they are given a hint.

                os.system('cls' if os.name == 'nt' else 'clear')
                print("Here's a hint!")
                playing_game.give_hint()
                playing_game.got_help = True
                print(playing_game.board)
                

                # Check after every play whether the game is solved and then saves game and score
                if playing_game.win_condition():
                    break

                continue

            elif play == "3":
                # If the player requests it, the full solution is displayed.

                print("Here is the solution:")
                playing_game.step_auto()
                playing_game.got_help = True
                print(playing_game.board)

                # Check after every play whether the game is solved and then saves score
                if playing_game.win_condition():
                    playing_game.finish_game()
                break


            elif play == "4":
                # If the player wants to save, the game is paused and saved to a file.

                self.is_saved = True
                try:
                    playing_game.save_game(f"{self._save_path}")
                    print("Your game was successfully saved.")
                except FileNotFoundError:
                    print("The file was not found.")
                except IOError:
                    print("An error occurred while reading the file.")
                break

            else:
                print("Invalid option. Please select 1, 2, 3, or 4.")
                continue  # Re-ask for input

        
        
    def display(self):
        """
        Main function for managing user interactions with the UI.
        """

        try:
           # Attempt to open the file where user information is stored.
           self._user_manager.load()
        except FileNotFoundError:
           raise AttributeError("File not found!")
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            print("\n=== Main Menu ===")
            print("1) Register new user")
            print("2) Log in")
            print("3) Print Scoreboard")
            print("x) Exit")
            try:
                choice = input("Select an option: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nBye.")
                break # If the input is interrupted, end the session

            if choice == "1":
                # Create a new user based on the player's input.
                try:
                    self._user_manager.register()
                    print("Registration successful.")
                except ValueError as e:
                    print(f"Error: {e}", file=sys.stderr)
                except Exception as e:
                    print(f"Unexpected error: {e}", file=sys.stderr)

            elif choice == "2":
                # Log into an existing account and start playing a game.

                try:
                    self.is_saved = False
                    player = self._user_manager.login()
                    print(f"You are logged in as {player.name}. Starting game...")
                    mode = input("Do you want to start a new game? [y/n] ").lower()
                    if mode == "y":
                        os.system('cls' if os.name == 'nt' else 'clear')
                        while True:
                            # Ask for the difficulty and ensure the input is valid.

                            print("1) Really Easy")
                            print("2) Easy")
                            print("3) Medium")
                            print("4) Hard")
                            difficulty = input("Select a difficulty: ").strip().lower()

                            if difficulty in ["1", "really easy"]:
                                game = Game(player, self._highscore_manager, "really easy")
                                break # Exit loop if the input is valid
                            elif difficulty in ["2", "easy"]:
                                game = Game(player, self._highscore_manager, "easy")
                                break # Exit loop if the input is valid
                            elif difficulty in ["3", "medium"]:
                                game = Game(player, self._highscore_manager, "medium")
                                break # Exit loop if the input is valid
                            elif difficulty in ["4", "hard"]:
                                game = Game(player, self._highscore_manager, "hard")
                                break # Exit loop if the input is valid
                            else:
                                os.system('cls' if os.name == 'nt' else 'clear')
                                print("Invalid input. Please select a valid difficulty (1-4).")

                        game.run()
                        print(game.board)
                        while not game.board.is_solved():
                            if self.is_saved == True:
                                # If the game was just saved, stop the playing loop.
                                break
                            self.playing_input(game)

                    elif mode == "n":
                        mode = input("Do you want to load a old game and continue playing? [y/n] ").lower()
                        if mode == "y":
                            # Load a previously saved game from file.
                            game_file = f"{self._save_path}"
                            game = Game.load_game(game_file, player, self._highscore_manager)
                            print(game.board)
                            game.run()
                            self.playing_input(game)
                            self._user_manager.update(player)
                        else:
                            exit(0)
                    else:
                        print("Invalid input. Please try again.")
                except ValueError as e:
                    print(f"Login failed: {e}", file=sys.stderr)
                except Exception as e:
                    print(f"Unexpected error: {e}", file=sys.stderr)

            elif choice == "3":
                # Print the scoreboard in a formatted way.
                print("Name:\tScore:\tTime:\t\tLevel:\tgot Hints:")
                for entry in self._highscore_manager.entries:
                    print(f"{entry}")

            elif choice == "x":
                # Allows the player to exit the program.
                print("Goodbye!")
                break

            else:
                 # Handle invalid menu input.
                print("Invalid choice. Please select 1, 2, 3, or x.")
                

    def start(self):
        """Starts the user interface."""
        self.display()
        

