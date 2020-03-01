from PySide2.QtWidgets import QGridLayout, QWidget
from src.gui.table.tile import Tile


class TableGrid(QGridLayout):
    def __init__(self):
        super(TableGrid, self).__init__()
        self.setSpacing(0)
        self.table = [[0]*8,[0]*8,[0]*8,[0]*8,[0]*8,[0]*8,[0]*8,[0]*8]
        self.generate_tiles()
        self.setMargin(10)

    def generate_tiles(self):
        for i in range(8):
            for j in range(8):
                if (i+j)%2 == 0:
                    color = "#aaa"
                else:
                    color = "#333"
                self.table[i][j] = Tile(color)
                self.addWidget(self.table[i][j], i, j)

