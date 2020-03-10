from PySide2.QtWidgets import QProgressBar, QSizePolicy
from PySide2.QtCore import Qt, QPropertyAnimation


class HeuristicBar(QProgressBar):
    def __init__(self):
        super(HeuristicBar, self).__init__()
        # centring text works, but still do no rotate it
        self.setStyleSheet("QProgressBar { text-align: center; background:#aaa;" +
                           " } QProgressBar::chunk {" +
                           "background: qlineargradient(x0:0, y0:0, x1:1, y1:0, stop:0 #222, stop:1 #333);" +
                           "border-radius: 5px;" +
                           "border-style: solid;" +
                           "border-width: 1px;" +
                           "border-color: #845;}")
        self.setOrientation(Qt.Vertical)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        # self.setMinimumWidth(60)
        self.setMinimum(-100)
        self.setMaximum(100)
        # self.setValue(0)
        self.setFormat("%p")
        self.animator = QPropertyAnimation(self, b"value")

    def animate_value(self, value):
        self.animator.stop()
        self.animator.setDuration(500)
        self.animator.setStartValue(self.value())
        self.animator.setEndValue(value)
        self.animator.start()
