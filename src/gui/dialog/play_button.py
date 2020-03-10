from PySide2.QtWidgets import QWidget, QLabel, QStyleOption, QStyle
from PySide2.QtCore import Qt, QAbstractAnimation, QVariantAnimation, QPropertyAnimation
from PySide2.QtGui import QPainter, QColor, QPalette


class PlayButton(QWidget):
    def __init__(self, parent):
        super(PlayButton, self).__init__(parent)
        self.parent = parent
        self.main_window = parent.main_window

        self.setStyleSheet("background: rgb(244,84,67,100);" +
                           "border-radius: 10;" +
                           "border-style: solid;" +
                           "border-width: 5px;" +
                           "border-color: #232;")
        self.label = QLabel(self)
        self.transition = None
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def restyle(self, bg):
        r,g,b,a = bg.red(), bg.green(), bg.blue(), bg.alpha()
        self.setStyleSheet("background: rgb("+str(r)+","+str(g)+","+str(b)+","+str(a)+");" +
                           "border-radius: 10;" +
                           "border-style: solid;" +
                           "border-width: 5px;" +
                           "border-color: #232;")

    def mousePressEvent(self, event):
        self.main_window.start_game(self.parent.is_force_move(), self.parent.is_pc_move(), self.parent.get_difficulty())
        self.parent.save_remembered()

    def enterEvent(self, event):
        super(PlayButton, self).enterEvent(event)
        self.animate_hover(True)

    def leaveEvent(self, event):
        super(PlayButton, self).leaveEvent(event)
        self.animate_hover(False)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def set_text(self, text):
        self.label.setText(text)
        self.label.move(0, 0)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background: transparent; color:white;")
        self.label.resize(self.width(), self.height())

        font = self.label.font()
        font.setBold(True)
        font.setPointSize(14)
        self.label.setFont(font)

    def update_size(self):
        self.resize(self.width(), self.height())
        self.label.resize(self.width(), self.height())

    def animate_hover(self, enter):
        base_color = QColor(244,84,67,100)
        hover_color = QColor(244,84,67,255)

        start_value = base_color if enter else hover_color

        if self.transition:
            start_value = self.transition.currentValue()
            self.transition.stop()

        self.transition = QPropertyAnimation(self, b"palete")

        self.transition.setStartValue(start_value)
        self.transition.setEndValue(hover_color if enter else base_color)
        self.transition.setDuration(100)
        self.transition.setDirection(QPropertyAnimation.Forward);
        self.transition.valueChanged.connect(lambda: self.restyle(self.transition.currentValue()))

        self.transition.start()
