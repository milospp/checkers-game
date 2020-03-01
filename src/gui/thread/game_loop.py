from src.chekcers import Stack, f_jump, config_print, Board
from PySide2.QtCore import QThread, QEventLoop
from src.gui.singals import PcMoveSignal, PlayerMoveSignal


class GameLoop(QThread):
    def __init__(self, parent=None):
        super(GameLoop, self).__init__(parent)
        self.signalPieces = PcMoveSignal()
        self.playerMove = PlayerMoveSignal()
        self.playerMove.moveToThread(self)
        # self.playerMove.sig.connect(self.stop_waiting)

    def run(self):
        # time_stack = Stack()
        # config_print()
        # f_jump()
        tabla1 = Board(pc_signal=self.signalPieces, player_signal=self.playerMove)
        tabla1.play_game()


