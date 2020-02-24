from src.chekcers import Stack, f_jump, config_print, Board
from src.gui.main_gui import main_gui

if __name__ == '__main__':
    main_gui()

    while True:
        time_stack = Stack()
        config_print()
        f_jump()
        tabla1 = Board()
        tabla1.play_game()
