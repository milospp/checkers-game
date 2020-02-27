from src.chekcers import Stack, f_jump, config_print, Board

from PySide2.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from src.gui.thread.game_loop import GameLoop
import sys

def main_gui():

    main_app = QApplication(sys.argv)

    main_app.main_window = MainWindow()
    main_app.main_window.show()
    #main_app.setStyle('fusion')
    #main_app.controller = MainController(main_app)
    game = GameLoop()
    game.start()

    sys.exit(main_app.exec_())
