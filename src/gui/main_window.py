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

        self.centerWidget = QWidget(self)
        self.center_layout = TableGrid()

        self.pieces = []
        self.grid = self.center_layout.table

        self.aspect_ratio_widget = AspectRatioWidget(self.centerWidget, None)

        self.draw_table()
        self.windows_adjustment()
        self.create_pieces()

    def windows_adjustment(self):
        self.setContentsMargins(0,0,0,0)
        self.setWindowTitle("Checkers")

        self.setMinimumSize(400, 400)
        self.resize(768, 768)

    def draw_table(self):

        self.centerWidget.setLayout(self.center_layout)
        self.setCentralWidget(self.aspect_ratio_widget)

    def create_pieces(self):
        pc = Piece(self.centerWidget)
        pc.raise_()
        self.pieces.append(pc)

    def resizeEvent(self, event):
        for i in self.pieces:
            i.update_size(event.size().width(), event.size().height(), self.grid)
