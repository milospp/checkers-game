from src.chekcers import Stack, f_jump, config_print, Board

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QThread
from src.gui.main_window import MainWindow
from src.gui.thread.game_loop import GameLoop
import sys

def main_gui():

    main_app = QApplication(sys.argv)
    QThread.currentThread().setPriority(QThread.HighPriority)

    main_app.main_window = MainWindow()
    main_app.main_window.show()
    #main_app.setStyle('fusion')
    #main_app.controller = MainController(main_app)


    sys.exit(main_app.exec_())
