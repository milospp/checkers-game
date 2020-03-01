from PySide2.QtWidgets import QWidget, QStyleOption, QStyle, QFrame
from PySide2.QtGui import QPainter, QCursor
from PySide2.QtCore import QPoint


class Piece(QFrame):
    def __init__(self, parent, piece_type, row, col, move=False):
        super(Piece, self).__init__(parent)
        self.main_window = parent.parent().parent()     # CenterWidget >> AspectRatioWidget >> MainWindow
        # self.move(0, 0)
        # self.resize(50, 50)
        self.setStyleSheet("background: " + "red; border-radius: 50px")
        self.border_radius = 10
        self.offset = QPoint()
        self.crs = QCursor()
        self.table_width = 50
        self.piece_type = piece_type
        self.col = col
        self.row = row
        self.movable = move
        self.possible_jumps = []

    def update_size(self, w, h):
        # print(grid[0][0].width())
        if w > h:
            self.table_width = h
        else:
            self.table_width = w
        width = (self.table_width-20) / 8
        # tile_size = grid[self.col][self.row].width()
        self.move(width * self.col + 10, width * self.row + 10)
        self.resize(width, width)
        self.border_radius = int(width/2)
        self.paint_piece()
        # self.setStyleSheet("background: " + "red; border-radius: " + str(int(width/2)) +"px")


    # StckOverflow
    # https://stackoverflow.com/questions/18344135/why-do-stylesheets-not-work-when-subclassing-qwidget-and-using-q-object
    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def mousePressEvent(self, event):
        super(Piece, self).mousePressEvent(event)
        self.offset = event.globalPos()-self.pos()

    def mouseMoveEvent(self, event):
        super(Piece, self).mouseMoveEvent(event)
        if self.movable:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        super(Piece, self).mouseReleaseEvent(event)
        # self.offset = event.globalPos()-self.pos()
        self.calc_position()

    def update_position(self):
        width = (self.table_width-20) / 8
        self.move(width * self.col + 10, width * self.row + 10)

    def calc_position(self):
        widget_size = self.table_width - 20
        cell_size = widget_size / 8
        x_center = self.pos().x() - 10 + cell_size / 2
        y_center = self.pos().y() - 10 + cell_size / 2
        new_col = int(x_center/cell_size)
        new_row = int(y_center/cell_size)
        if y_center >= 10 and new_row <= 7 and x_center >= 10 and new_col <= 7:
            if self.is_position_valid(new_row, new_col):
                old = [self.row, self.col]
                self.row = new_row
                self.col = new_col
                self.main_window.lock_pieces()
                # self.main_window.game.playerMove.sig.emit("test")
                self.main_window.game.playerMove.stop_waiting([old, [self.row, self.col]])  # Stop eventloop in singals.py
        self.update_position()

    def is_position_valid(self,row,col):
        for jmp in self.possible_jumps:
            if row == jmp[0] and col == jmp[1]:
                return True
        return False

    def paint_piece(self):
        color = get_piece_color(self.piece_type)
        border_width = (self.table_width - 20) / 8 / 8
        if self.piece_type == 4 or self.piece_type == 5:
            border_radius = self.border_radius - 5
            border_color = "#a32"

        else:
            border_radius = self.border_radius
            border_color = "#999"
            border_width /= 2


        self.setStyleSheet("background: " + str(color) + ";" +
                           "border-radius: " + str(border_radius) + "px;" +
                           "border-style: outset;" +
                           "border-width: " + str(border_width) + "px;" +
                           "border-color: " + border_color + ";")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        # self.setFrameStyle(QFrame.Raised)
        self.setLineWidth(20)

def get_piece_color(type):
    if type == 1:           #Player a
        return "#222"
    elif type == 2:         #PC a
        return "#bbb"
    elif type == 3:
        return "#777"
    elif type == 4:         #Player b
        return "#111"
    elif type == 5:         #PC b
        return "#ccc"
    return "red"