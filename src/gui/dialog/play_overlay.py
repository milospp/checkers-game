from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout
from PySide2.QtCore import Qt, QTimer
from src.gui.dialog.play_button import PlayButton


class PlayOverlay(QWidget):

    def __init__(self, parent, status):
        super(PlayOverlay, self).__init__(parent)
        self.status = status
        self.main_widget = parent
        self.main_window = parent.parent()  # AspectRatioWidget >> MainWindow

        self.resize(self.main_window.size().width(), self.main_window.size().height())
        self.resize(100, 100)

        self.gridLayout = QGridLayout()
        self.label = QLabel(self)
        self.btn_play = PlayButton(self)
        self.btn_force_jump = QPushButton(self)
        self.btn_pc_first = QPushButton(self)

        self.btn_lvl1 = QPushButton(self)
        self.btn_lvl2 = QPushButton(self)
        self.btn_lvl3 = QPushButton(self)

        self.btn_undo = QPushButton(self)

        self.init_layout()
        self.set_remembered()

    def resizeEvent(self, event):
        super(PlayOverlay, self).resizeEvent(event)
        w = event.size().width()
        h = event.size().height()
        self.update_sizes(w, h)

    def update_sizes(self, width, height):
        self.resize(width, height)
        y = height / 2 - 370
        self.label.resize(width, 500)
        self.label.move(0, y)

        y = height / 2
        x = width / 2

        self.btn_play.move(x - 150, y - 20)

        self.btn_force_jump.move(x - 150, y + 60)
        self.btn_pc_first.move(x, y + 60)
        self.btn_undo.move(x - 100, y - 70)

        self.btn_lvl1.move(x - 150, y + 120)
        self.btn_lvl2.move(x - 50, y + 120)
        self.btn_lvl3.move(x + 50, y + 120)

        if width < 600:
            pt_size = 38
        else:
            pt_size = 72

        font = self.label.font()
        font.setPointSize(pt_size)
        font.setBold(True)
        self.label.setFont(font)

    def init_layout(self):
        self.label.setObjectName("status")
        self.label.setText(self.get_status_string())
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background: transparent; color:#ddd")

        font = self.label.font()
        font.setPointSize(72)
        font.setBold(True)
        self.label.setFont(font)

        self.btn_play.resize(300, 70)

        self.btn_force_jump.setText("Force Jump")
        self.btn_force_jump.setCheckable(True)
        self.btn_force_jump.resize(150, 50)

        self.btn_pc_first.setText("PC First")
        self.btn_pc_first.setCheckable(True)
        self.btn_pc_first.resize(150, 50)
        # self.btn_play.move(100,200)

        self.btn_lvl1.resize(100, 50)
        self.btn_lvl2.resize(100, 50)
        self.btn_lvl3.resize(100, 50)

        self.btn_lvl1.setCheckable(True)
        self.btn_lvl2.setCheckable(True)
        self.btn_lvl3.setCheckable(True)
        self.btn_lvl1.setText("EASY")
        self.btn_lvl2.setText("MEDIUM")
        self.btn_lvl3.setText("HARD")
        self.btn_lvl1.clicked.connect(lambda: self.difficulty_radio(1))
        self.btn_lvl2.clicked.connect(lambda: self.difficulty_radio(2))
        self.btn_lvl3.clicked.connect(lambda: self.difficulty_radio(3))
        self.difficulty_radio(2)

        self.btn_undo.setText("UNDO")
        self.btn_undo.resize(200, 40)
        self.btn_undo.clicked.connect(self.undo_move)

        if self.status == -1:
            self.btn_play.set_text("PLAY")
            self.btn_undo.setVisible(False)
        else:
            self.btn_play.set_text("PLAY AGAIN")
            if self.main_window.history_table:
                self.btn_undo.setVisible(True)
            else:
                self.btn_undo.setVisible(False)

        self.btn_play.show()

    def get_status_string(self):
        if self.status == 0:
            return "Draw"
        elif self.status == 1:
            return "You win"
        elif self.status == 2:
            return "You lose"
        elif self.status == 3:
            return "Draw (win)"
        elif self.status == 4:
            return "Draw (lose)"
        elif self.status == -1:
            return "Checkers"
        elif self.status == -2:
            return "Checkers"

    def difficulty_radio(self, btn_id):
        self.btn_lvl1.setChecked(False)
        self.btn_lvl3.setChecked(False)
        self.btn_lvl2.setChecked(False)
        if btn_id == 1:
            self.btn_lvl1.setChecked(True)
        elif btn_id == 2:
            self.btn_lvl2.setChecked(True)
        elif btn_id == 3:
            self.btn_lvl3.setChecked(True)

    def is_force_move(self):
        return self.btn_force_jump.isChecked()

    def is_pc_move(self):
        return self.btn_pc_first.isChecked()

    def get_radio_selected(self):
        if self.btn_lvl3.isChecked():
            return 3
        elif self.btn_lvl2.isChecked():
            return 2
        elif self.btn_lvl1.isChecked():
            return 1
        else:
            return 2

    def get_difficulty(self):
        if self.btn_lvl3.isChecked():
            return 5
        elif self.btn_lvl2.isChecked():
            return 4
        elif self.btn_lvl1.isChecked():
            return 3
        else:
            return 4

    def undo_move(self):
        remembered = self.main_window.remember_choice_config
        undo = self.main_window.history_table.pop()
        matrix = undo[0]
        self.main_window.start_game(remembered[0], False, remembered[2], matrix)
        # heuristic bar is updated 50ms so it will happend after, because this undo create new game with 'undo'
        # starting matrix
        QTimer.singleShot(50, lambda: self.main_window.update_heuristic_bar(undo[1]))

    def set_remembered(self):
        remembered = self.main_window.remember_choice_config
        self.btn_force_jump.setChecked(remembered[0])
        self.btn_pc_first.setChecked(remembered[1])
        self.difficulty_radio(remembered[2])

    def save_remembered(self):
        self.main_window.remember_choice_config[0] = self.btn_force_jump.isChecked()
        self.main_window.remember_choice_config[1] = self.btn_pc_first.isChecked()
        self.main_window.remember_choice_config[2] = self.get_radio_selected()
