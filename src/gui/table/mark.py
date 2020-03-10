from PySide2.QtWidgets import QWidget, QStyleOption, QStyle, QGraphicsOpacityEffect
from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter


class Mark(QWidget):

    def __init__(self, parent, row, col):
        super(Mark, self).__init__(parent)
        self.main_window = parent.parent().parent().parent()     # CenterWidget >> AspectRatioWidget >> MainWindow

        self.table_width = 50
        self.row = row
        self.col = col

        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.op = QGraphicsOpacityEffect(self)
        self.op.setOpacity(0.50)  # 0 to 1 will cause the fade effect to kick in
        self.setGraphicsEffect(self.op)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def update_size(self, w, h):
        side_width = self.main_window.aspect_ratio_widget.side_widget.width()

        if w - side_width > h:
            self.table_width = h
        else:
            self.table_width = w - side_width
        cell_width = (self.table_width-20) / 8
        width = cell_width / 4
        self.setStyleSheet("border-radius: " + str(width/2-1) + "px; background: white; opacity:0.5;")
        self.resize(width, width)
        self.move(cell_width * self.col + 3*width/2 + 10, cell_width * self.row + 3*width/2 + 10)

