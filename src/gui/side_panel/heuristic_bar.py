from PySide2.QtWidgets import QProgressBar, QSizePolicy
from PySide2.QtCore import Qt

class HeuristicBar(QProgressBar):
    def __init__(self):
        super(HeuristicBar, self).__init__()
        # centring text works, but still do no rotate it
        self.setStyleSheet("QProgressBar { text-align: center; } SSSQProgressBar::chunk {border-radius:20}")
        self.setOrientation(Qt.Vertical)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        # self.setMinimumWidth(60)
        self.setMinimum(-100)
        self.setMaximum(100)
        self.setValue(40)
        self.setFormat("%p")