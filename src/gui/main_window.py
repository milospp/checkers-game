from src.gui.thread.game_loop import GameLoop
from PySide2.QtWidgets import QMainWindow, QWidget, QGridLayout, QBoxLayout, QHBoxLayout
from PySide2.QtCore import QTimer
from PySide2.QtGui import QPainter, QBrush, QColor
from PySide2.QtCore import QThread
from src.gui.table.table_grid import TableGrid
from src.gui.table.piece import Piece
from src.gui.table.mark import Mark
from src.gui.dialog.play_overlay import PlayOverlay
from src.gui.dialog.black_overlay import BlackOverlay
from src.gui.aspect_ratio_widget import AspectRatioWidget
from src.chekcers import last_jump_to_list
import time


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.game = GameLoop(self)

        self.centerWidget = QWidget(self)
        self.center_layout = TableGrid(self)

        self.pieces = []
        self.pieces_matrix = [[0]*8]*8
        self.grid = self.center_layout.table
        self.available_moves = []
        self.current_matrix = []

        self.animation_timer_list = []
        self.animation_shrink_list = []

        self.mark_source = []
        self.marks = []
        self.pl_last_eat = []

        self.overlayBG = None
        self.overlay = None

        self.aspect_ratio_widget = AspectRatioWidget(self.centerWidget, None)

        self.draw_table()
        self.windows_adjustment()
        self.show_menu(-1)

        # self.init_game_thread()

    def windows_adjustment(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle("Checkers")

        self.setMinimumSize(400, 400)
        self.resize(768, 768)

    def draw_table(self):
        self.centerWidget.setLayout(self.center_layout)
        self.setCentralWidget(self.aspect_ratio_widget)

    def resizeEvent(self, event):
        for i in self.pieces:
            i.update_size(event.size().width(), event.size().height())

        for i in self.marks:
            i.update_size(event.size().width(), event.size().height())

        if self.overlay:
            self.overlay.resizeEvent(event)
            self.overlayBG.resizeEvent(event)

    def init_game_thread(self):
        self.game.start(QThread.LowPriority)
        self.game.signalPieces.sig.connect(self.pc_piece_move)

    # Player_move control should move be animated
    def pc_piece_move(self, jump, matrix, all_moves, moved=True):
        self.available_moves = all_moves
        self.current_matrix = matrix
        self.update_movable_tag()

        # Player jumped, pieces is moved by gui, no need to repalce anything
        if not moved and jump:
            return

        if not moved:
            self.replace_matrix(matrix)
            self.update_movable_tag()
            return

        if jump:
            self.pl_last_eat = []

            jump_list = last_jump_to_list(jump)
            rng = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
            wait_animation = 0  # Used to create delay when pc move after promotion
            # timer = QTimer()
            self.animation_timer_list = []
            self.animation_shrink_list = []

            eated_list = []
            for i, one_jump in enumerate(jump_list):
                jump_from = one_jump[0]
                jump_to = one_jump[1]
                self.print_matrix()
                mov_piece = self.pieces_matrix[jump_list[0][0][0]][jump_list[0][0][1]]

                self.animation_timer_list.append(QTimer())
                self.animation_timer_list[-1].setSingleShot(True)
                self.animation_timer_list[-1].setInterval(500*i+wait_animation)
                self.animation_timer_list[-1].timeout.connect(lambda: mov_piece.animate_move(jump_list[rng[0]][1][0], jump_list[rng.pop(0)][1][1]))
                self.animation_timer_list[-1].start()

                if abs(jump_from[0] - jump_to[0]) == 2:
                    ate_x = int((jump_from[0] + jump_to[0])/2)
                    ate_y = int((jump_from[1] + jump_to[1])/2)

                    eated_list.append([ate_x, ate_y])

                    self.animation_shrink_list.append(QTimer())
                    self.animation_shrink_list[-1].setSingleShot(True)
                    self.animation_shrink_list[-1].setInterval(500*i+wait_animation+250)
                    self.animation_shrink_list[-1].timeout.connect(
                        lambda: self.shrink_piece(eated_list[0][0],eated_list.pop(0)[1]))
                    self.animation_shrink_list[-1].start()

                    # QTimer.singleShot(500*i+wait_animation+250, lambda: self.shrink_piece(eated_list[0][0],eated_list.pop(0)[1]))
                    # QTimer.singleShot(500*i+wait_animation+250, lambda: self.pieces_matrix[eated_list[0][0]][eated_list.pop(0)[1]].shrink_animation())
                    #     # self.main_window.pieces_matrix[ate_x][ate_y].shrink_animation()
                    #     # self.shrink_animation

                if jump_to[0] == 7:
                    wait_animation = 200

            self.animation_timer_list.append(QTimer())
            self.animation_timer_list[-1].setSingleShot(True)
            self.animation_timer_list[-1].setInterval(500*i+500+wait_animation)
            self.animation_timer_list[-1].timeout.connect(self.replace_matrix)
            self.animation_timer_list[-1].timeout.connect(lambda: self.animation_timer_list.clear())
            self.animation_timer_list[-1].start()
            # self.time.singleShot(500*i+500+wait_animation, self.replace_matrix)

            # self.update_movable_tag()

    def shrink_piece(self,i,j):
        if self.pieces_matrix[i][j]:
            self.pieces_matrix[i][j].shrink_animation()

    def replace_matrix(self, matrix=None, no_edit=None):
        if no_edit:
            ne_x = no_edit.row
            ne_y = no_edit.col
        else:
            ne_x, ne_y = -1, -1

        if not matrix:
            mx = self.current_matrix
        else:
            mx = matrix
        self.remove_pieces(no_edit)
        self.pieces = []    # Delete pieces?
        self.pieces_matrix = [[0]*8,[0]*8,[0]*8,[0]*8,[0]*8,[0]*8,[0]*8,[0]*8]
        for i in range(8):
            for j in range(8):
                piece_type = mx[i][j]
                if i == ne_x and j == ne_y:

                    # Keep if is on same place
                    if no_edit.piece_type == piece_type:
                        self.pieces_matrix[i][j] = no_edit
                        self.pieces.append(no_edit)

                        continue
                    else:
                        no_edit.close()

                if piece_type != 0 and piece_type != 3 and piece_type != 6:
                    pc = Piece(self.centerWidget, piece_type, i, j)
                    pc.raise_()
                    pc.show()
                    self.pieces.append(pc)
                    self.pieces_matrix[i][j] = pc

        for i in self.pieces:
            i.update_size(self.size().width(), self.size().height())
        self.update_movable_tag()

    def update_movable_tag(self):
        jump_piece = None
        for piece in self.pieces:
            piece.possible_jumps.clear()

        for mov in self.available_moves:
            i = mov[0][0]
            j = mov[0][1]
            if self.pieces_matrix[i][j]:
                self.pieces_matrix[i][j].movable = True
                self.pieces_matrix[i][j].possible_jumps.append(mov[1])
            if mov[0] == self.pl_last_eat and abs(mov[1][0] - self.pl_last_eat[0]) == 2:
                jump_piece = self.pieces_matrix[mov[0][0]][mov[0][1]]
        if jump_piece:
            self.create_marks(jump_piece.possible_jumps)
            self.mark_source = [jump_piece.row, jump_piece.col]
            jump_piece.confirm_jump_stop = True

    def click_on_tile(self, i, j):
        # print(i,j)
        for mark in self.marks:
            x1, y1 = self.mark_source[0], self.mark_source[1]

            if mark.row == i and mark.col == j:
                # x1,y1 = self.mark_source[0], self.mark_source[1]
                x2,y2 = mark.row, mark.col

                if self.pieces_matrix[x1][y1]:
                    print("zvanje animacije")
                    self.pieces_matrix[x1][y1].animate_pl_move(x2, y2)
                # self.pieces_matrix[x1][y1].calc_position()
            else:
                self.pieces_matrix[x1][y1].confirm_jump_stop = False
                # self.confirm_jump_stop

        self.remove_marks(True)

    def lock_pieces(self):
        for piece in self.pieces:
            piece.movable = False

    def remove_pieces(self, exclude=None):
        for i in self.pieces:
            if exclude and exclude == i:
                continue
            i.close()

    def remove_marks(self, clear_list=True):
        for i in self.marks:
            i.close()
        if clear_list:
            self.marks.clear()

    def create_marks(self, positions):
        for pos in positions:
            mark = Mark(self.centerWidget, pos[0], pos[1])
            mark.raise_()
            mark.show()
            mark.update_size(self.size().width(), self.size().height())
            self.marks.append(mark)

    def show_menu(self, status, check_animation=True):
        # a = QTimer()
        # a.remainingTime()
        if check_animation:
            if self.animation_timer_list:
                remaining = self.animation_timer_list[-1].remainingTime()
                self.animation_timer_list.append(QTimer())
                self.animation_timer_list[-1].setSingleShot(True)
                self.animation_timer_list[-1].setInterval(remaining)
                self.animation_timer_list[-1].setObjectName("end")
                self.animation_timer_list[-1].timeout.connect(lambda: self.show_menu(status, False))
                self.animation_timer_list[-1].start()
                return

        bo = BlackOverlay(self.aspect_ratio_widget)
        bo.raise_()
        bo.show()
        end = PlayOverlay(self.aspect_ratio_widget, status)
        end.raise_()
        end.show()

        w = self.width()
        h = self.height()
        bo.resize(w, h)
        end.resize(w, h)

        self.overlayBG = bo
        self.overlay = end

    def start_game(self):
        print("START GAME")
        for i in self.animation_shrink_list:
            i.stop()

        self.remove_pieces()
        self.pieces.clear()
        self.pieces_matrix = [[0]*8]*8
        self.available_moves.clear()
        self.current_matrix.clear()
        self.animation_timer_list.clear()
        self.mark_source.clear()
        self.marks.clear()

        self.overlay.close()
        self.overlayBG.close()
        self.game.exit()
        self.game = GameLoop(self)

        self.init_game_thread()

    def print_matrix(self):
        for i in self.pieces_matrix:
            for j in i:
                if j == 0:
                    print("0 ", end="")
                else:
                    print(str(j.piece_type) + " ", end="")
            print()
        print("----------")

