from PySide2.QtWidgets import QWidget, QStyleOption, QStyle, QLabel, QPushButton, QGridLayout, QGraphicsOpacityEffect
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt
from src.gui.dialog.play_button import PlayButton


class PlayOverlay(QWidget):

    def __init__(self, parent, status):
        super(PlayOverlay, self).__init__(parent)
        self.status = status
        self.main_widget = parent
        self.main_window = parent.parent()     # AspectRatioWidget >> MainWindow

        self.resize(self.main_window.size().width(), self.main_window.size().height())
        self.resize(100,100)

        self.gridLayout = QGridLayout()
        self.label = QLabel(self)
        self.btn_play = PlayButton(self)

        self.init_layout()

    def resizeEvent(self, event):
        super(PlayOverlay, self).resizeEvent(event)
        w = event.size().width()
        h = event.size().height()
        self.update_sizes(w, h)

    def update_sizes(self, width, height):
        self.resize(width, height)
        y = height/2-370
        self.label.resize(width,500)
        self.label.move(0, y)

        y = height/2
        x = width/2 - 150

        self.btn_play.move(x, y)
        self.btn_play.update_size()

        if width < 600:
            pt_size = 38
        else:
            pt_size = 72

        font = self.label.font()
        font.setPointSize(pt_size)
        font.setBold(True)
        self.label.setFont(font)



    def mousePressEvent(self, event):
        super(PlayOverlay, self).mousePressEvent(event)
        # self.resize(self.main_widget.width(), self.main_widget.height())

    # def paintEvent(self, pe):
    #     o = QStyleOption()
    #     o.initFrom(self)
    #     p = QPainter(self)
    #     self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def init_layout(self):
        self.label.setObjectName("status")
        self.label.setText(self.get_status_string())
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background: transparent; color:#ddd")

        font = self.label.font()
        font.setPointSize(72)
        font.setBold(True)
        self.label.setFont(font)

        self.btn_play.resize(300,70)
        self.btn_play.move(100,200)
        if self.status == -1:
            self.btn_play.set_text("PLAY")
        else:
            self.btn_play.set_text("PLAY AGAIN")

        self.btn_play.show()
        # font = self.btn_play.font()
        # font.setPointSize(12)
        # font.setBold(True)
        # self.btn_play.setFont(font)


        self.resize(500,400)


        # self.setLayout(self.gridLayout)
        # self.gridLayout.addWidget(self.label, 0, 0)
        # self.gridLayout.addWidget(self.btn_play, 1, 0)


    # def update_position(self):
    def get_status_string(self):
        if self.status == 0:
            return "Draw"
        elif self.status == 1:
            return "You win"
        elif self.status == 2:
            return "You lose"
        elif self.status == 3:
            return "Draw (win)"
        elif self.status == 4:
            return "Draw (lose)"
        elif self.status == -1:
            return "Checkers"
