from PySide2.QtWidgets import QWidget, QStyleOption, QStyle, QFrame, QGraphicsDropShadowEffect
from PySide2.QtGui import QPainter, QCursor
from PySide2.QtCore import QPoint, QPropertyAnimation, QRect, QTimer, QThread


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
        self.animator = QPropertyAnimation(self, b"geometry")
        self.styles = {}

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(0)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.setGraphicsEffect(self.shadow)
        self.confirm_jump_stop = False

    def update_size(self, w, h):
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

    def resizeEvent(self, event):
        super(Piece, self).resizeEvent(event)
        width = event.size().width()

        if self.styles:
            self.setStyleSheet("background: " + self.styles["background"] + ";" +
                               "border-radius: " + str(width/2-2) + "px;" +
                               "border-style: outset;" +
                               "border-width: " + self.styles["border-width"] + "px;" +
                               "border-color: " + self.styles["border-color"] + ";")

    def enterEvent(self, event):
        if self.movable:
            self.move(self.pos().x()-10, self.pos().y()-10)
            self.shadow.setBlurRadius(5)
            self.shadow.setXOffset(10)
            self.shadow.setYOffset(10)

    def leaveEvent(self, event):
        if self.movable:
            self.update_position()
            self.shadow.setBlurRadius(0)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)

    def mousePressEvent(self, event):

        super(Piece, self).mousePressEvent(event)
        # print("mousepressevent")
        self.main_window.remove_marks(True)
        if self.movable:
            self.main_window.create_marks(self.possible_jumps)
            self.main_window.mark_source = [self.row, self.col]
        self.offset = event.globalPos()-self.pos()

        # Cancel all animation and replace matrix
        if self.main_window.animation_timer_list:
            for timer in self.main_window.animation_timer_list:
                if timer.objectName() == "end":
                    self.main_window.replace_matrix()
                    timer.setInterval(10)
                    return
                timer.stop()
            self.possible_jumps.clear()
            self.main_window.replace_matrix(None, self)
            self.main_window.animation_timer_list = []

    def mouseMoveEvent(self, event):
        # print("Move event, Piece")
        super(Piece, self).mouseMoveEvent(event)
        self.raise_()
        # self.confirm_jump_stop = True
        if self.movable:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        super(Piece, self).mouseReleaseEvent(event)
        self.shadow.setBlurRadius(0)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        # self.offset = event.globalPos()-self.pos()
        if self.movable:

            self.calc_position(True)

    def update_position(self):
        width = (self.table_width-20) / 8
        self.move(width * self.col + 10, width * self.row + 10)

    def calc_position(self, user=False):
        widget_size = self.table_width - 20
        cell_size = widget_size / 8
        x_center = self.pos().x() - 10 + cell_size / 2
        y_center = self.pos().y() - 10 + cell_size / 2
        new_col = int(x_center/cell_size)
        new_row = int(y_center/cell_size)
        if user and new_row == self.row and new_col == self.col:
            if [new_row, new_col] in self.possible_jumps:
                if not self.confirm_jump_stop:
                    self.confirm_jump_stop = True
                    return
            else:
                return
        self.confirm_jump_stop = False

        if y_center >= 10 and new_row <= 7 and x_center >= 10 and new_col <= 7:
            if self.is_position_valid(new_row, new_col):
                self.main_window.remove_marks(True)

                self.movable = False
                self.main_window.pieces_matrix[self.row][self.col] = 0
                self.main_window.pieces_matrix[new_row][new_col] = self
                old = [self.row, self.col]

                self.row = new_row
                self.col = new_col
                self.main_window.lock_pieces()
                if self.row == 0:
                    if self.piece_type == 1:
                        self.piece_type = 4
                    self.paint_piece()
                    # elif self.piece_type == 2:
                    #     self.piece_type = 5
                    # QTimer.singleShot(500, self.paint_piece)
                # self.main_window.game.playerMove.sig.emit("test")
                print("Piece pred zvanje",[old, [self.row, self.col]], user)


                QTimer.singleShot(10, lambda: self.main_window.game.playerMove.stop_waiting([old, [self.row, self.col]]))

                if abs(new_row - old[0]) == 2:
                    ate_x = int((new_row + old[0])/2)
                    ate_y = int((new_col + old[1])/2)
                    self.main_window.pieces_matrix[ate_x][ate_y].shrink_animation()
                    self.main_window.pl_last_eat = [new_row, new_col]
                else:
                    self.main_window.pl_last_eat = []
                # self.main_window.game.playerMove.stop_waiting([old, [self.row, self.col]])  # Stop eventloop in singals.py

        print("Update position")
        self.update_position()

    def is_position_valid(self, row, col):
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
            if self.piece_type == 1:
                border_color = "#444"
            else:
                border_color = "#999"

            border_width /= 2

        self.styles["background"] = str(color)
        self.styles["border-radius"] = str(border_radius)
        self.styles["border-style"] = "outset"
        self.styles["border-width"] = str(border_width)
        self.styles["border-color"] = border_color

        self.setStyleSheet("background: " + str(color) + ";" +
                           "border-radius: " + str(border_radius) + "px;" +
                           "border-style: outset;" +
                           "border-width: " + str(border_width) + "px;" +
                           "border-color: " + border_color + ";")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        # self.setFrameStyle(QFrame.Raised)
        # self.setLineWidth(20)

        # if self.movable:
        #     self.shadow.setBlurRadius(5)
        #     self.shadow.setXOffset(10)
        #     self.shadow.setYOffset(10)
        # else:
        #     self.shadow.setBlurRadius(0)
        #     self.shadow.setXOffset(0)
        #     self.shadow.setYOffset(0)

    def animate_move(self, i, j):
        self.raise_()
        self.animator.stop()
        y = (self.table_width - 20) / 8 * i + 10
        x = (self.table_width - 20) / 8 * j + 10
        old_rect = QRect(self.pos().x(), self.pos().y(), self.width(), self.height())
        rect = QRect(x, y, self.height(), self.width())
        self.animator.setDuration(500)
        self.animator.setStartValue(old_rect)
        self.animator.setEndValue(rect)
        self.animator.start()
        self.main_window.pieces_matrix[i][j] = self.main_window.pieces_matrix[self.row][self.col]
        self.main_window.pieces_matrix[self.row][self.col] = 0

        # if abs(self.row - i) == 2:
        #     QTimer.singleShot(10, lambda: self.main_window.pieces_matrix[ate_x][ate_y]())
        #     # self.main_window.pieces_matrix[ate_x][ate_y].shrink_animation()
        #     # self.shrink_animation

        self.row = i
        self.col = j
        if self.row == 7:
            if self.piece_type == 1:
                self.piece_type = 4
            elif self.piece_type == 2:
                self.piece_type = 5
            QTimer.singleShot(500, self.paint_piece)

    def animate_pl_move(self, i, j):
        if not self.is_position_valid(i,j):
            print("Piece, ne mnoze move")
            return
        self.raise_()
        self.animator.stop()
        self.animator = QPropertyAnimation(self, b"geometry")
        y = (self.table_width - 20) / 8 * i + 10
        x = (self.table_width - 20) / 8 * j + 10
        old_rect = QRect(self.pos().x(), self.pos().y(), self.width(), self.height())
        rect = QRect(x, y, self.height(), self.width())
        self.animator.setDuration(500)
        self.animator.setStartValue(old_rect)
        self.animator.setEndValue(rect)
        self.animator.finished.connect(self.calc_position)

        self.animator.start()

    def shrink_animation(self):
        tile_width = (self.table_width-20) / 8
        self.animator.stop()
        old_rect = QRect(self.pos().x(), self.pos().y(), self.width(), self.height())
        rect = QRect(self.pos().x() + tile_width/2, self.pos().y() + tile_width/2, 0, 0)
        self.animator.setDuration(500)
        self.animator.setStartValue(old_rect)
        self.animator.setEndValue(rect)
        self.styleSheet()
        self.animator.start()


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