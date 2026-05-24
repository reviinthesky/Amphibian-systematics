from src.identifier import Identifier
from src.ui import *
from src.input_handler import normalize_input


def main():
    user_input = run_questionier()
    user_input = normalize_input(user_input)
    app = Identifier()
    top3, winner, percentage = app.find_matches(user_input)
    if winner is None:
        show_failed_window()
        return
    else:
        show_result_window(top3, winner, percentage)


if __name__ == '__main__':
    main()
