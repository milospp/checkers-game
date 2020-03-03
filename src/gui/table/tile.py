from PySide2.QtWidgets import QWidget, QStyleOption, QStyle, QSizePolicy
from PySide2.QtGui import QPainter
from PySide2.QtCore import Qt


class Tile(QWidget):
    def __init__(self, color):
        super(Tile, self).__init__()
        self.setStyleSheet("background: " + color + ";")


    def mousePressEvent(self, event):
        print("Prees")

    # StckOverflow
    # https://stackoverflow.com/questions/18344135/why-do-stylesheets-not-work-when-subclassing-qwidget-and-using-q-object
    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

