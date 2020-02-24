from PySide2.QtWidgets import QWidget, QStyleOption, QStyle, QSizePolicy
from PySide2.QtGui import QPainter


class Tile(QWidget):
    def __init__(self, color):
        super(Tile, self).__init__()
        self.setStyleSheet("background: " + color)


        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)

    def heightForWidth(self, arg__1):
        return self.width()

    def hasHeightForWidth(self):
        return True

    # StckOverflow
    # https://stackoverflow.com/questions/18344135/why-do-stylesheets-not-work-when-subclassing-qwidget-and-using-q-object
    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

