from src.gui.thread.game_loop import GameLoop
from PySide2.QtWidgets import QMainWindow, QWidget, QGridLayout, QBoxLayout, QHBoxLayout
from PySide2.QtGui import QPainter, QBrush, QColor
from PySide2.QtCore import Qt
from src.gui.table.table_grid import TableGrid
from src.gui.table.piece import Piece
from src.gui.aspect_ratio_widget import AspectRatioWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.game = GameLoop()

        self.centerWidget = QWidget(self)
        self.center_layout = TableGrid()

        self.pieces = []
        self.grid = self.center_layout.table

        self.aspect_ratio_widget = AspectRatioWidget(self.centerWidget, None)

        self.draw_table()
        self.windows_adjustment()
        self.init_game_thread()

    def windows_adjustment(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle("Checkers")

        self.setMinimumSize(400, 400)
        self.resize(768, 768)

    def draw_table(self):
        self.centerWidget.setLayout(self.center_layout)
        self.setCentralWidget(self.aspect_ratio_widget)

    def create_pieces(self):
        pc = Piece(self.centerWidget, 2, 2, 1)
        pc.raise_()
        self.pieces.append(pc)

    def resizeEvent(self, event):
        for i in self.pieces:
            i.update_size(event.size().width(), event.size().height())

    def init_game_thread(self):
        self.game.start()
        self.game.signalPieces.sig.connect(self.piece_move)

    def piece_move(self, jump, matrix, all_moves):
        if not jump:
            self.replace_matrix(matrix)

    def replace_matrix(self, matrix):
        self.remove_pieces()
        self.pieces = []    # Delete pieces?
        for i in range(8):
            for j in range(8):
                piece_type = matrix[i][j]
                if piece_type != 0:
                    pc = Piece(self.centerWidget, piece_type, i, j)
                    pc.raise_()
                    pc.show()
                    self.pieces.append(pc)


        for i in self.pieces:
            i.update_size(self.size().width(), self.size().height())

    def remove_pieces(self):
        for i in self.pieces:
            i.close()


    # def testsig(self, jump, matrix, moves):
    #     print("RADI SIGNAAL")
    #     print(matrix)
    #     print(jump)
    #     print(moves)
    #     print("----")
