from PySide2.QtWidgets import QWidget, QStyleOption, QStyle, QSizePolicy
from PySide2.QtGui import QPainter
from PySide2.QtCore import Qt


class Tile(QWidget):
    def __init__(self, parent, color, row, col):
        super(Tile, self).__init__()
        self.setStyleSheet("background: " + color + ";")
        self.main_window = parent

        self.row = row
        self.col = col

    def mousePressEvent(self, event):
        self.main_window.click_on_tile(self.row, self.col)

    # StckOverflow
    # https://stackoverflow.com/questions/18344135/why-do-stylesheets-not-work-when-subclassing-qwidget-and-using-q-object
    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

