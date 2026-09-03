import sys

from user_interface.user_interface import UI
from utils.highscore_manager import HighScoreManager
from utils.user_manager import UserManager

def main(usr_path: str, hs_path: str, sv_path: str) -> None:
    """
    Main function

    Args:
        usr_path: Path to user folder
        hs_path: Path to highscore folder
        sv_path: Path to score folder
    """
    try:
        u = UserManager(usr_path)
        h = HighScoreManager(hs_path)
        h.load()

        UI(user_manager=u, highscore_manager=h, save_path=sv_path).start()
    except KeyboardInterrupt:
        print("\nBye.")
    except AttributeError as e:
        print(f"Error: {e}", file=sys.stderr)
if __name__ == '__main__':
    """
    Main entry point of the program to start a game with tui (terminal ui).
    """

    user_path = "./save_data/players.txt"
    high_score_path = "./save_data/highscores.txt"
    save_path = "./save_data/saves.json"

    if "-o" in sys.argv:
        if len(sys.argv) != 5:
            print("When using the -o option, you need to specify the output file path.")
            print("Usage: main.py -o <user_path> <highscore_path> <save_path>")
            exit(1)
        user_path = sys.argv[1]
        high_score_path = sys.argv[2]
        save_path = sys.argv[3]

    main(usr_path=user_path, hs_path=high_score_path, sv_path=save_path)
