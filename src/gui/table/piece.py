from PySide2.QtWidgets import QWidget, QStyleOption, QStyle
from PySide2.QtGui import QPainter, QCursor
from PySide2.QtCore import QPoint


class Piece(QWidget):
    def __init__(self, parent):
        super(Piece, self).__init__(parent)
        self.move(0, 0)
        # self.resize(50, 50)
        self.setStyleSheet("background: " + "red; border-radius: 50px")
        self.offset = QPoint()
        self.crs = QCursor()
        self.col = 5
        self.row = 6

    def update_size(self, w, h, grid):
        print(grid[0][0].width())
        if w > h:
            width = h - 20
        else:
            width = w-20

        tile_size = grid[self.col][self.row].width()
        self.move(width / 8 * self.col + 10, width / 8 * self.row + 10)
        self.resize(width/8, width/8)
        self.setStyleSheet("background: " + "red; border-radius: " + str(int(width/16)) +"px")


    # StckOverflow
    # https://stackoverflow.com/questions/18344135/why-do-stylesheets-not-work-when-subclassing-qwidget-and-using-q-object
    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def mousePressEvent(self, event):
        super(Piece, self).mousePressEvent(event)
        self.offset = event.globalPos()-self.pos()

    def mouseMoveEvent(self, event):
        super(Piece, self).mouseMoveEvent(event)
        self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        super(Piece, self).mouseReleaseEvent(event)
        self.offset = event.globalPos()-self.pos()
