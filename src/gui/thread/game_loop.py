from src.chekcers import Stack, f_jump, config_print, Board
from PySide2.QtCore import QThread, QEventLoop
from src.gui.singals import PcMoveSignal, PlayerMoveSignal, FinishSignal
import time


class GameLoop(QThread):
    def __init__(self, parent=None, force_move=None, pc_first=None, depth=5, matrix=None):
        super(GameLoop, self).__init__(parent)
        self.game_param = [force_move, pc_first, depth, matrix]
        self.main_window = parent
        self.signalPieces = PcMoveSignal()
        self.playerMove = PlayerMoveSignal(self)
        self.playerMove.moveToThread(self)
        self.finishSignal = FinishSignal()
        self.finishSignal.sig.connect(self.main_window.show_menu)
        # self.finishSignal.sig.connect(lambda: print("Sta je ovo"))
        # self.playerMove.moveToThread(self.thread())
        # self.playerMove.sig.connect(self.stop_waiting)show_menu

    def run(self):
        # time_stack = Stack()
        # config_print()
        # f_jump()

        tabla1 = Board(game_param = self.game_param, pc_signal=self.signalPieces, player_signal=self.playerMove, finish_signal=self.finishSignal)
        tabla1.play_game()


# class SignalWait(QThread):
#     def __init__(self, param, parent=None):
#         super(SignalWait, self).__init__(parent)
#         self.main_window = parent
#         self.param = param
#         # self.playerMove.sig.connect(self.stop_waiting)show_menu
#
#     def run(self):
#         print("sleep start")
#         time.sleep(2)
#         print("sleep end")
#         self.main_window.game.playerMove.stop_waiting(self.param)
#
