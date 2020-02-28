from src.chekcers import Stack, f_jump, config_print, Board
from PySide2.QtCore import QThread, Signal
from src.gui.singals import PcMoveSignal


class GameLoop(QThread):
    def __init__(self, parent=None):
        super(GameLoop, self).__init__(parent)
        self.signalPieces = PcMoveSignal()
        #self.exiting = False

    def run(self):
        # time_stack = Stack()
        # config_print()
        # f_jump()
        tabla1 = Board(signal=self.signalPieces)
        tabla1.play_game()