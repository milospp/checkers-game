from PySide2.QtWidgets import QWidget, QStyleOption, QStyle, QSizePolicy, QVBoxLayout, QPushButton
from PySide2.QtGui import QPainter
from PySide2.QtCore import QMargins
from src.gui.side_panel.heuristic_bar import HeuristicBar


class SidePanel(QWidget):
    def __init__(self, parent):
        super(SidePanel, self).__init__(parent)
        self.main_window = parent
        self.setLayout(QVBoxLayout())
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred))
        self.setMinimumWidth(70)
        self.setMaximumWidth(70)
        self.layout().setContentsMargins(QMargins(0, 10, 10, 10))
        # self.layout().setSpacing(0)

        self.btn_more = QPushButton("Menu")
        self.btn_undo = QPushButton("<---")
        self.btn_redo = QPushButton("--->")
        self.progress_bar = HeuristicBar()
        self.init_layout()

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def init_layout(self):
        self.layout().addWidget(self.btn_more)
        self.layout().addWidget(self.progress_bar)
        self.layout().addWidget(self.btn_undo)
        self.layout().addWidget(self.btn_redo)

        self.btn_more.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        self.btn_undo.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        self.btn_redo.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        self.btn_more.setMinimumHeight(60)
        self.btn_undo.setMinimumHeight(30)
        self.btn_redo.setMinimumHeight(30)
        self.btn_undo.setDisabled(True)
        self.btn_redo.setDisabled(True)

        self.btn_undo.clicked.connect(self.main_window.undo_move)
        self.btn_redo.clicked.connect(self.main_window.redo_move)
        self.btn_more.clicked.connect(lambda: self.main_window.show_menu(-2, False))
