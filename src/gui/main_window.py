from PySide2.QtWidgets import QMainWindow, QWidget, QSizePolicy, QBoxLayout, QHBoxLayout
from PySide2.QtGui import QPainter, QBrush, QColor
from PySide2.QtCore import Qt
from src.gui.table.table_grid import TableGrid


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.aspect_ratio = self.size().width() / self.size().height()
        self.color = QColor(0, 0, 0)


        self.centerWidget = QWidget()
        self.center_layout = TableGrid()
        self.centerWidget.setLayout(self.center_layout)
        self.container = QHBoxLayout()
        self.container.addWidget(self.centerWidget)



        self.setCentralWidget(self.centerWidget)
        self.setWindowTitle("Checkers")

        self.setDocumentMode(False)
        self.setMinimumSize(500, 400)
        self.resize(1024, 768)
        self.centerWidget.resize(200,200)


#    def resizeEvent(self, e):

