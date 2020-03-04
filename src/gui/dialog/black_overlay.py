from PySide2.QtWidgets import QWidget, QStyleOption, QStyle, QLabel, QPushButton, QGridLayout, QGraphicsOpacityEffect
from PySide2.QtGui import QPainter


class BlackOverlay(QWidget):

    def __init__(self, parent):
        super(BlackOverlay, self).__init__(parent)
        self.main_widget = parent
        self.main_window = parent.parent()     # AspectRatioWidget >> MainWindow

        self.resize(self.main_window.size().width(), self.main_window.size().height())

        self.op = QGraphicsOpacityEffect(self)

        self.init_layout()

    def resizeEvent(self, event):
        super(BlackOverlay, self).resizeEvent(event)
        w = event.size().width()
        h = event.size().height()
        self.resize(w,h)

    # def mousePressEvent(self, event):
    #     super(End, self).mousePressEvent(event)
    #     # print("ss", self.main_widget.height(), "sss")
    #     # self.resize(self.main_widget.width(), self.main_widget.height())

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def init_layout(self):

        self.op.setOpacity(0.50)  # 0 to 1 will cause the fade effect to kick in
        self.setGraphicsEffect(self.op)

    # def update_position(self):
