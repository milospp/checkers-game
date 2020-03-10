from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QThread
from src.gui.main_window import MainWindow
import sys


def main_gui():
    main_app = QApplication(sys.argv)
    QThread.currentThread().setPriority(QThread.HighPriority)

    main_app.setStyle('fusion')
    main_app.main_window = MainWindow()
    main_app.main_window.show()
    # main_app.controller = MainController(main_app)

    sys.exit(main_app.exec_())
