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
from src.gui.side_panel.side_panel import SidePanel
from copy import deepcopy
import time


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.game = GameLoop(self)
        self.remember_choice_config = [False, False, 2]

        self.centerWidget = QWidget(self)
        self.center_layout = TableGrid(self)

        self.sideWidget = SidePanel(self)

        self.pieces = []
        self.pieces_matrix = [[0]*8]*8
        self.grid = self.center_layout.table
        self.available_moves = []
        self.current_matrix = []
        self.current_heuristic = None

        # Undo table is saved after every pc move, but if PC plays first, we cant save table before 1st move
        self.pc_first_jump = True

        self.animation_timer_list = []
        self.animation_shrink_list = []

        self.mark_source = []
        self.marks = []
        self.pl_last_eat = []
        self.history_table = []
        self.history_redo = []

        self.overlayBG = None
        self.overlay = None

        self.aspect_ratio_widget = AspectRatioWidget(self.centerWidget, self.sideWidget, None)

        self.setStyleSheet("background:#333;")
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
            # i.update_size(self.centerWidget.width(), self.centerWidget.height())
            i.update_size(event.size().width(), event.size().height())

        for i in self.marks:
            # i.update_size(self.centerWidget.width(), self.centerWidget.height())
            i.update_size(event.size().width(), event.size().height())

        if self.overlay:
            self.overlay.resizeEvent(event)
            self.overlayBG.resizeEvent(event)

    def init_game_thread(self):
        self.game.start(QThread.LowPriority)
        self.game.signalPieces.sig.connect(self.pc_piece_move)

    # Player_move control should move be animated
    def pc_piece_move(self, jump, matrix, all_moves, moved=True, heuristic_value = None):
        self.available_moves = all_moves
        old_matrix = self.current_matrix
        self.current_matrix = deepcopy(matrix)
        self.update_movable_tag()

        # Player jumped, pieces is moved by gui, no need to repalce anything
        if not moved and jump:
            print("NOT MOVED AND JUMP")
            self.history_table.append([deepcopy(old_matrix), self.current_heuristic])

            return
        self.remove_marks(True)

        if not moved:
            self.replace_matrix(matrix)
            self.update_movable_tag()
            if self.current_heuristic is None:
                self.current_heuristic = heuristic_value
                self.update_heuristic_bar(heuristic_value)
            return

        if jump:
            self.pl_last_eat = []
            self.history_redo.clear()

            if self.pc_first_jump and self.remember_choice_config[1]:
                self.pc_first_jump = False
            else:
                self.history_table.append([deepcopy(old_matrix), self.current_heuristic])
            self.current_heuristic = heuristic_value

            self.update_undo_redo_btn()

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
                        lambda: self.shrink_piece(eated_list[0][0], eated_list.pop(0)[1]))
                    self.animation_shrink_list[-1].start()

                if jump_to[0] == 7:
                    wait_animation = 200


            self.animation_timer_list.append(QTimer())
            self.animation_timer_list[-1].setSingleShot(True)
            self.animation_timer_list[-1].setInterval(500*i+500+wait_animation)
            self.animation_timer_list[-1].timeout.connect(self.replace_matrix)
            self.animation_timer_list[-1].timeout.connect(lambda: self.animation_timer_list.clear())
            self.animation_timer_list[-1].start()

            self.update_heuristic_bar(self.current_heuristic)
            # End of if jump

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
        for mark in self.marks:
            x1, y1 = self.mark_source[0], self.mark_source[1]

            if mark.row == i and mark.col == j:
                # x1,y1 = self.mark_source[0], self.mark_source[1]
                x2,y2 = mark.row, mark.col

                if self.pieces_matrix[x1][y1]:
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
            # mark.update_size(self.centerWidget.width(), self.centerWidget.height())
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
        if self.overlayBG:
            if self.overlayBG.isVisible():
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

    def start_game(self, force_move=False, pc_first=False, depth=5, matrix=None):
        for i in self.animation_shrink_list:
            i.stop()

        self.remove_pieces()
        self.pieces.clear()
        self.pieces_matrix = [[0]*8]*8
        self.available_moves.clear()
        self.current_matrix.clear()
        self.current_heuristic = None
        self.pc_first_jump = True
        self.animation_timer_list.clear()
        self.remove_marks(True)
        self.mark_source.clear()

        # matix is sent as starting table in new game, if we click undo in the end of game
        if not matrix:
            self.history_table.clear()
            self.history_redo.clear()

        self.overlay.close()
        self.overlayBG.close()
        self.game.terminate()
        self.game = GameLoop(self, force_move, pc_first, depth, matrix)

        self.init_game_thread()

    def undo_move(self):
        if self.history_table:
            self.history_redo.append([deepcopy(self.current_matrix), self.current_heuristic])
            undo = self.history_table.pop()
            self.game.playerMove.stop_waiting([-1, undo[0]])
            self.current_heuristic = undo[1]
            self.update_heuristic_bar(self.current_heuristic)
            self.update_undo_redo_btn()

    def redo_move(self):
        if self.history_redo:
            self.history_table.append([deepcopy(self.current_matrix), self.current_heuristic])
            redo = self.history_redo.pop()
            self.game.playerMove.stop_waiting([-1, redo[0]])
            self.current_heuristic = redo[1]
            self.update_heuristic_bar(self.current_heuristic)
            self.update_undo_redo_btn()

    def update_undo_redo_btn(self):
        if self.history_table:
            self.sideWidget.btn_undo.setDisabled(False)
        else:
            self.sideWidget.btn_undo.setDisabled(True)
        if self.history_redo:
            self.sideWidget.btn_redo.setDisabled(False)
        else:
            self.sideWidget.btn_redo.setDisabled(True)

    def update_heuristic_bar(self, value):
        bar = self.sideWidget.progress_bar

        if value == 900:
            value = 100
        elif value == -900:
            value = -100
        elif value >= 99:
            value = 99
        elif value <= -99:
            value = -99

        value = -value

        bar.animate_value(value)

    def clear_overlay(self):
        self.overlayBG.close()
        self.overlay.close()

    def print_matrix(self):
        for i in self.pieces_matrix:
            for j in i:
                if j == 0:
                    print("0 ", end="")
                else:
                    print(str(j.piece_type) + " ", end="")
            print()
        print("----------")

