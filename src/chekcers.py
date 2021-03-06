import copy
import time
import random


def minimax(node, depth_ab, alpha, beta, maximizing):
    # if depth_ab == depth - 1:
    #     time.sleep(0.01)
    # def minimax(node, depth, maximizing):
    if depth_ab == 0:  # or game OVER
        node.calc()
        return node

    if maximizing:
        max_value = -999
        generate(node, 2, depth_ab)
        if not node.children:
            node.value = -900
            return Node(-900)
        for child in node.children:
            calc = minimax(child, depth_ab - 1, alpha, beta, False)
            # calc = minimax(child, depth-1, False)
            max_value = max(max_value, calc)
            alpha = max(calc, alpha)
            if beta <= alpha:
                break
        node.value = max_value.value
        return max_value
    else:
        min_value = 999
        generate(node, 1, depth_ab)
        if not node.children:
            node.value = 900
            return Node(900)
        for child in node.children:
            # calc = minimax(child, depth-1, True)
            calc = minimax(child, depth_ab - 1, alpha, beta, True)
            min_value = min(min_value, calc)
            beta = min(calc, beta)
            if beta <= alpha:
                break
        node.value = min_value.value
        return min_value


class Node(object):
    def __init__(self, value=None, board=None):
        self.board = board
        self.value = value
        self.children = []

    def calc(self):
        # print(self.board.calculate())
        self.value = self.board.calculate()
        # sprint(self.value)

    def add_child(self, obj):
        self.children.append(obj)

    def get_value(self):
        return self.value

    def __str__(self, level=0):
        return str(self.board) + " | " + str(self.value)

    # def __cmp__(self, other):
    #     input("OPAA")
    #     return cmp(self.value, other.value)

    def __lt__(self, other):
        if isinstance(other, Node):
            other = other.value
        return self.value < other if True else False

    def __le__(self, other):
        if isinstance(other, Node):
            other = other.value
        return self.value <= other if True else False

    def __gt__(self, other):
        if isinstance(other, Node):
            other = other.value
        return self.value > other if True else False

    def __ge__(self, other):
        if isinstance(other, Node):
            other = other.value
        return self.value >= other if True else False

    def treeview(self, level=0):
        ret = "\t" * level + repr(self.value) + "\n"
        for child in self.children:
            ret += child.treeview(level + 1)
        return ret


class Stack:
    def __init__(self, items=[]):
        if items:
            self.items = items
        else:
            self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def set(self, elements=[]):
        self.items = elements

    def three_sum(self):
        return self.items[-1] + self.items[-2] + self.items[-3]


class Board(object):
    def __init__(self, new_matrix=None, last_jmp=None, game_param=None, pc_signal=None, player_signal=None,
                 finish_signal=None):
        if not new_matrix:
            self.matrix = [[0, 2, 0, 2, 0, 2, 0, 2],
                           [2, 0, 2, 0, 2, 0, 2, 0],
                           [0, 2, 0, 2, 0, 2, 0, 2],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [1, 0, 1, 0, 1, 0, 1, 0],
                           [0, 1, 0, 1, 0, 1, 0, 1],
                           [1, 0, 1, 0, 1, 0, 1, 0]]

            # self.matrix = [[0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [5, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [1, 0, 0, 0, 0, 0, 0, 0]]

            # self.matrix = [[0, 2, 0, 2, 0, 2, 0, 2],
            #                [2, 0, 2, 0, 2, 0, 2, 0],
            #                [0, 2, 0, 2, 0, 2, 0, 2],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [1, 0, 2, 0, 1, 0, 1, 0],
            #                [0, 1, 0, 1, 0, 1, 0, 1],
            #                [1, 0, 1, 0, 1, 0, 1, 0]]

            # self.matrix = [[0, 0, 0, 0, 0, 0, 0, 0],
            #                [2, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [1, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 1, 0, 1, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 1, 0, 1, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0]]
            #

            # self.matrix = [[0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 2, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 2, 0, 2, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 2, 0, 0, 0, 0, 0],
            #                [0, 1, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0]]

            # self.matrix = [[0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0],
            #                [0, 0, 0, 0, 0, 0, 0, 0]]

        else:
            self.matrix = new_matrix
        if last_jmp:
            self.lastjump = last_jmp
        else:
            self.lastjump = []

        if game_param:
            global depth, force_jump, pc_first, variable_depth
            force_jump = game_param[0]
            pc_first = game_param[1]
            depth = game_param[2]
            if depth != 5:
                variable_depth = False
            if game_param[3]:
                self.matrix = copy.deepcopy(game_param[3])

        self.minimax_heuristic = None
        self.signal = pc_signal
        self.player_signal = player_signal
        self.finish_signal = finish_signal

    def get_matrix(self):
        return self.matrix

    def calculate(self):
        value = 0
        for enum_i, i in enumerate(self.matrix):
            for enum_j, j in enumerate(i):
                if j == 0:
                    continue
                if j == 1: value -= 5 + 7 - enum_i + abs(enum_j - 4) + abs(enum_i - 4)
                if j == 2: value += 5 + enum_i + abs(enum_j - 4) + abs(enum_i - 4)
                if j == 4: value -= 14 + abs(enum_j - 4) + abs(enum_i - 4)
                if j == 5: value += 14 + abs(enum_j - 4) + abs(enum_i - 4)

        return value

    def count_figures(self):
        value = 0
        for enum_i, i in enumerate(self.matrix):
            for enum_j, j in enumerate(i):
                if j == 1: value -= 1
                if j == 2: value += 1
                if j == 4: value -= 2
                if j == 5: value += 2

        return value

    def possible_moves(self, param):  # param = 1 - PLAYER, param = 2 - PC
        moves = []
        force_moves = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 0 or self.matrix[i][j] % 3 != param:
                    continue
                #  print(i,j)
                vertical = 1 if param == 2 else -1  # ako je param = 1, to su PC figure koje idu dole
                enemy = 1 if param == 2 else 2
                cell = self.matrix[i][j]
                if j - 1 != -1 and i + vertical != -1 and i + vertical != 8 and \
                        self.matrix[i + vertical][j - 1] % 3 != param:
                    if j - 2 > -1 and 8 > i + vertical * 2 > -1 and self.matrix[i + vertical][j - 1] % 3 == enemy and \
                            self.matrix[i + vertical * 2][j - 2] % 3 == 0:
                        # print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical*2) + ", " + str(j - 2))
                        moves.append([[i, j], [i + vertical * 2, j - 2]])
                        force_moves.append([[i, j], [i + vertical * 2, j - 2]])
                    elif self.matrix[i + vertical][j - 1] % 3 == 0:
                        # print(str(i) + ", " + str(j) + " => " + str(i+vertical) + ", " + str(j-1))
                        moves.append([[i, j], [i + vertical, j - 1]])
                if j + 1 != 8 and i + vertical != -1 and i + vertical != 8 and \
                        self.matrix[i + vertical][j + 1] % 3 != param:
                    if j + 2 < 8 and 8 > i + vertical * 2 > -1 and self.matrix[i + vertical][j + 1] % 3 == enemy and \
                            self.matrix[i + vertical * 2][j + 2] % 3 == 0:
                        # print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical*2) + ", " + str(j + 2))
                        moves.append([[i, j], [i + vertical * 2, j + 2]])
                        force_moves.append([[i, j], [i + vertical * 2, j + 2]])
                    elif self.matrix[i + vertical][j + 1] % 3 == 0:
                        # print(str(i) + ", " + str(j) + " => " + str(i + vertical) + ", " + str(j + 1) + "*")
                        moves.append([[i, j], [i + vertical, j + 1]])
                if cell > 3:
                    if j - 1 != -1 and i - vertical != -1 and i - vertical != 8 and \
                            self.matrix[i - vertical][j - 1] % 3 != param:
                        if j - 2 > -1 and 8 > i - vertical * 2 > -1 and \
                                self.matrix[i - vertical][j - 1] % 3 == enemy and \
                                self.matrix[i - vertical * 2][j - 2] % 3 == 0:
                            # print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical*2) + ", " + str(j - 2))
                            moves.append([[i, j], [i - vertical * 2, j - 2]])
                            force_moves.append([[i, j], [i - vertical * 2, j - 2]])
                        elif self.matrix[i - vertical][j - 1] % 3 == 0:
                            # print(str(i) + ", " + str(j) + " => " + str(i-vertical) + ", " + str(j-1))
                            moves.append([[i, j], [i - vertical, j - 1]])
                    if j + 1 != 8 and i - vertical != -1 and i - vertical != 8 and \
                            self.matrix[i - vertical][j + 1] % 3 != param:
                        if j + 2 < 8 and 8 > i - vertical * 2 > -1 and \
                                self.matrix[i - vertical][j + 1] % 3 == enemy and \
                                self.matrix[i - vertical * 2][j + 2] % 3 == 0:
                            # print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical*2) + ", " + str(j + 2))
                            moves.append([[i, j], [i - vertical * 2, j + 2]])
                            force_moves.append([[i, j], [i - vertical * 2, j + 2]])
                        elif self.matrix[i - vertical][j + 1] % 3 == 0:
                            # print(str(i) + ", " + str(j) + " => " + str(i + vertical) + ", " + str(j + 1) + "*")
                            moves.append([[i, j], [i - vertical, j + 1]])
        if force_jump and force_moves:
            return force_moves
        else:
            return moves

    def eatable(self, param, i, j):
        moves = [[[i, j], [i, j]]]
        vertical = 1 if param == 2 else -1
        enemy = 1 if param == 2 else 2
        cell = self.matrix[i][j]
        # print(self.matrix)

        if j - 1 != -1 and i + vertical != -1 and i + vertical != 8 and self.matrix[i + vertical][j - 1] % 3 == enemy:
            if j - 2 > -1 and 8 > i + vertical * 2 > -1 and self.matrix[i + vertical * 2][j - 2] % 3 == 0:
                # print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical * 2) + ", " + str(j - 2))
                moves.append([[i, j], [i + vertical * 2, j - 2]])
                # moves.extend(self.eatable(param, i+2, j-2))
        if j + 1 != 8 and i + vertical != -1 and i + vertical != 8 and self.matrix[i + vertical][j + 1] % 3 == enemy:
            if j + 2 < 8 and 8 > i + vertical * 2 > -1 and self.matrix[i + vertical * 2][j + 2] % 3 == 0:
                # print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical * 2) + ", " + str(j + 2))
                moves.append([[i, j], [i + vertical * 2, j + 2]])
                # moves.extend(self.eatable(param, i + 2, j + 2))

        if cell > 3:
            if j - 1 != -1 and i - vertical != -1 and i - vertical != 8 and \
                    self.matrix[i - vertical][j - 1] % 3 == enemy:
                if j - 2 > -1 and 8 > i - vertical * 2 > -1 and self.matrix[i - vertical * 2][j - 2] % 3 == 0:
                    # print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical * 2) + ", " + str(j - 2))
                    moves.append([[i, j], [i - vertical * 2, j - 2]])
                    # moves.extend(self.eatable(param, i+2, j-2))
            if j + 1 != 8 and i - vertical != -1 and i - vertical != 8 and \
                    self.matrix[i - vertical][j + 1] % 3 == enemy:

                if j + 2 < 8 and 8 > i - vertical * 2 > -1 and self.matrix[i - vertical * 2][j + 2] % 3 == 0:
                    # print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical * 2) + ", " + str(j + 2))
                    moves.append([[i, j], [i - vertical * 2, j + 2]])
                    # moves.extend(self.eatable(param, i + 2, j + 2))
        return moves

    def move(self, old, new, param=1, first_layer_depth=True):
        cell = self.matrix[old[0]][old[1]]
        self.matrix[old[0]][old[1]] = 3
        if (new[0] == 7 or new[0] == 0) and cell < 3:
            self.matrix[new[0]][new[1]] = cell + 3
        else:
            self.matrix[new[0]][new[1]] = cell
        if abs(old[0] - new[0]) == 2:
            # self.lastjump += str(chr(old[0] + 65)) + str(old[1] + 1) + " --> " + str(chr(new[0] + 65)) + str(
            #     new[1] + 1) + " (" + str(chr(int((old[0] + new[0]) / 2) + 65)) + str(
            #     int((old[1] + new[1]) / 2) + 1) + ")" + "\n"

            # A2 -> C4 (B3) is [01, 23, 12]
            # A == 0; B == 1...
            if first_layer_depth:
                self.lastjump.append(old[0] * 1000 + old[1] * 100 + new[0] * 10 + new[1])

            self.matrix[int((old[0] + new[0]) / 2)][int((old[1] + new[1]) / 2)] = 6
            eatable_cells = self.eatable(param, new[0], new[1])
            if len(eatable_cells) > 1:
                if param == 1:
                    # print("Ima jos da se jede PLAYER")
                    return 2
                else:
                    # print("Ima jos da se jede PC")
                    return 3
            return 4  # Pojeo
        # self.lastjump += str(chr(old[0] + 65)) + str(old[1] + 1) + " --> " + str(chr(new[0] + 65)) + str(
        #     new[1] + 1) + "\n"
        if first_layer_depth:
            self.lastjump.append(old[0] * 1000 + old[1] * 100 + new[0] * 10 + new[1])

        return 1  # Samo MOVE

    def pc_move(self, stack):
        root = Node(0, self)
        time1 = time.time()
        self.minimax_heuristic = minimax(root, depth, Node(-1000), Node(1000), True)
        think = time.time() - time1
        print("Thinking (sec):", think)
        stack.push(think)

        if not root.children:
            return 0

        self.matrix = copy.deepcopy(max(root.children).board.matrix)
        self.lastjump = copy.deepcopy(max(root.children).board.lastjump)
        return 1

    def clear_table_trails(self):
        for enum_i, i in enumerate(self.matrix):
            for enum_j, j in enumerate(i):
                if self.matrix[enum_i][enum_j] == 3 or self.matrix[enum_i][enum_j] == 6:
                    self.matrix[enum_i][enum_j] = 0

    def print(self, highlighted=0, moves=[], clear_trails=False):
        return
        print("HV Value:", self.calculate())
        print("Turn:", turn)

        cells = []
        order = 0
        if highlighted == 1:
            all_moves = self.possible_moves(1)
            for cell in all_moves:
                if cell[0] not in cells:
                    cells.append(cell[0])
            if not cells:
                return None

        print("     1     2     3     4     5     6      7      8")
        print("  |" + "－－－|" * 8)
        for enum_i, i in enumerate(self.matrix):
            print(str(chr(enum_i + 65)), end=" |")
            for enum_j, j in enumerate(i):
                if j == 0: j = " "
                if j == 1: j = v1
                if j == 2: j = v2
                if j == 3: j = v3
                if j == 4: j = v4
                if j == 5: j = v5
                if j == 6: j = v6

                num = " "
                try:
                    if highlighted == 1 and cells[0][0] == enum_i and cells[0][1] == enum_j:
                        order += 1
                        num = order
                        cells.pop(0)

                    if highlighted == 2:
                        # print(moves)
                        num = moves.index([enum_i, enum_j]) + 1
                        if num == 0:
                            num = " "
                except ValueError:
                    pass
                except IndexError:
                    pass

                print(" " + str(num) + str(j), end="   |")
                # print("  " + num + str(j), end="    ❙")
                if clear_trails and (self.matrix[enum_i][enum_j] == 3 or self.matrix[enum_i][enum_j] == 6):
                    self.matrix[enum_i][enum_j] = 0
            print("\n  |" + "－－－|" * 8)
        # if highlighted != 5:
        # print(self.lastjump)
        # last_jump_to_str(self.lastjump)

    def send_signal(self, explicit_move=None, new_move=True):
        if not self.signal:
            return None
        if explicit_move:
            # 4th arg is for updating position of table pieces
            self.signal.sig.emit(self.lastjump, self.matrix, explicit_move, new_move, None)
        else:

            if self.minimax_heuristic is not None:
                if self.minimax_heuristic.value > 400:
                    minimax_heuristic_value = 900
                elif self.minimax_heuristic.value < -400:
                    minimax_heuristic_value = -900
                else:
                    minimax_heuristic_value = accurate_calculate(self.minimax_heuristic.board.get_matrix())
            else:
                minimax_heuristic_value = accurate_calculate(self.get_matrix())

            self.signal.sig.emit(copy.deepcopy(self.lastjump), copy.deepcopy(self.matrix), self.possible_moves(1),
                                 new_move, minimax_heuristic_value)

    def play_game(self):
        global status, turn, depth
        turn = 0
        stack = Stack([4, 3, 3])
        self.send_signal(new_move=False)

        if pc_first:
            pc_moves = self.possible_moves(2)
            rand_move = random.choice(pc_moves)
            self.move(rand_move[0], rand_move[1], 2)
        while True:
            if variable_depth and (stack.three_sum() > 11 or stack.peek() > 4.5):
                depth -= 1
                stack.set([4, 4, 4])
                print("Smanjena dubina  na", depth)
            elif variable_depth and (stack.three_sum() < 2):
                depth += 1
                stack.set([4, 4, 4])
                print("Povećana dubina  na", depth)
            turn += 1
            self.print(1)
            self.send_signal(new_move=True)
            self.lastjump[:] = []
            if turn > 80:
                count = self.count_figures()
                if count > 0:
                    status = "Računar je u prednosti"
                    self.finish_message(4)
                    return 0
                elif count < 0:
                    status = "Igrač je u prednosti"
                    self.finish_message(3)
                    return 1
                else:
                    status = "Nerešeno"
                    self.finish_message(0)
                    return 3

            # Player move
            play = self.pl_move()
            # print("checkers.py Player zavrsio")
            if not play:
                status = "Računar je pobedio"
                self.finish_message(2)
                return 0
            self.print(clear_trails=True)

            turn += 1
            self.print(clear_trails=False)
            print("==PC==")
            self.lastjump[:] = []

            play = self.pc_move(stack)
            time.sleep(0.1)
            if not play:
                status = "Pobedili ste!"
                self.finish_message(1)
                return 1

    def pl_move(self, param=1, explicit=None):
        if self.player_signal:  # If GUI exist call another function that does not require input from keyboard
            return self.pl_gui_move(explicit)

        # self.pc_move(None, 1)
        all_moves = self.possible_moves(param)
        cells = []
        ready_moves = []
        if not explicit:
            for cell in all_moves:
                if cell[0] not in cells:
                    cells.append(cell[0])
            if not cells:
                return None

            # print(cells)
            print_moves(cells)
            while True:
                cell_num = input("Unesite broj celije: ")

                # print("--- Poziv pauze ---")
                # self.player_signal.wait_for_move()

                if cell_num.isnumeric():
                    cell_num = int(cell_num) - 1
                    if 0 <= cell_num < len(cells):
                        break
            position = cells[cell_num]
            for moves in all_moves:
                if moves[0] == [cells[cell_num][0], cells[cell_num][1]]:
                    ready_moves.append(moves[1])
        else:
            for pmoves in explicit:
                ready_moves.append(pmoves[1])
            position = explicit[0][0]
        # print(ready_moves)
        self.print(2, copy.deepcopy(ready_moves))
        print_moves(ready_moves)

        while True:
            r_broj = input("Unesite redni broj poteza")
            if r_broj.isnumeric():
                r_broj = int(r_broj) - 1
                if 0 <= int(r_broj) < len(ready_moves):
                    break
        if self.move(position, ready_moves[int(r_broj)]) == 2:
            next_hop = self.eatable(1, ready_moves[int(r_broj)][0], ready_moves[int(r_broj)][1])
            self.print()
            self.pl_move(1, next_hop)
        return 1

    def pl_gui_move(self, explicit=None):
        if not self.possible_moves(1):
            return None
        if not explicit:
            gui_move = self.player_signal.wait_for_move()
            if gui_move[0] == -1:
                if not gui_move[1]:
                    return None
                self.matrix = copy.deepcopy(gui_move[1])
                self.send_signal(new_move=False)

                return self.pl_gui_move()
            # print("primio signal 1")

        else:
            self.send_signal(explicit, new_move=False)
            gui_move = self.player_signal.wait_for_move()
            if gui_move[0] == -1:
                if not gui_move[1]:
                    return None
                self.matrix = copy.deepcopy(gui_move[1])
                self.send_signal(new_move=False)

                return self.pl_gui_move()
            # print("primio signal 2 exp")

        # print([gui_move[0], gui_move[1]])
        if self.move(gui_move[0], gui_move[1]) == 2:
            next_hop = self.eatable(1, gui_move[1][0], gui_move[1][1])
            self.print()
            self.pl_gui_move(next_hop)
        return 1

    def finish_message(self, s):
        self.finish_signal.sig.emit(s)


def generate(node, param, depth_ab):
    table = node.board
    for move in table.possible_moves(param):
        next_hop_add(node, table, move, param, depth_ab)


def next_hop_add(node, table, move, param, depth_ab):
    first_layer_depth = True if depth_ab == depth else False
    # first_layer_depth = True

    temp_new_table = Board(copy.deepcopy(table.matrix))
    if first_layer_depth:
        temp_new_table.lastjump = copy.deepcopy(table.lastjump)
    if temp_new_table.move(move[0], move[1], param, first_layer_depth=first_layer_depth) > 1:
        next_hop = temp_new_table.eatable(param, move[1][0], move[1][1])
        if len(next_hop) > 1:
            for n_move in next_hop[1:]:
                next_hop_add(node, temp_new_table, n_move, param, depth_ab)

    # new_table = Board([1,23])
    new_table = Board(copy.deepcopy(table.matrix))
    if first_layer_depth:
        new_table.lastjump = copy.deepcopy(table.lastjump)
    new_table.move(move[0], move[1], param, first_layer_depth=first_layer_depth)
    node.add_child(Node(None, new_table))
    return


def accurate_calculate(matrix):
    value = 0
    for enum_i, i in enumerate(matrix):
        for enum_j, j in enumerate(i):
            horizontal = abs(enum_j - 3) if enum_j < 4 else abs(enum_j - 4)
            vertical = abs(enum_i - 3) if enum_i < 4 else abs(enum_i - 4)
            if j == 1: value -= 5 + 7 - enum_i + horizontal + vertical
            if j == 2: value += 5 + enum_i + horizontal + vertical
            if j == 4: value -= 14 + horizontal + vertical
            if j == 5: value += 14 + horizontal + vertical

    return value


def print_moves(moves):
    for i, move in enumerate(moves):
        # print(chr(move[0]+65))
        print(str(i + 1) + ") " + str(chr(move[0] + 65)) + str(move[1] + 1), end="   |  ")
    print()


def player_move():
    pass


def f_jump():
    global status
    global force_jump
    global pc_first
    opt1 = "X"
    opt2 = "X"
    while True:
        print("\n" * 15)
        print("\n", status, "\n")
        print("1)", "[" + opt1 + "]", "Obavezan skok")
        print("2)", "[" + opt2 + "]", "Računar igra prvi")
        print("9)", "Izlaz")
        print("\tENTER za potvrdu\n")
        user_input = input("Izaberite opciju: ")
        if user_input == "":
            break
        if user_input.isnumeric():
            if int(user_input) == 1:
                opt1 = "O" if opt1 == "X" else "X"
                print(opt1)
            if int(user_input) == 2:
                opt2 = "O" if opt2 == "X" else "X"
            if int(user_input) == 9:
                exit()

    force_jump = True if opt1 == "O" else False
    pc_first = True if opt2 == "O" else False


def config_print():
    global v1, v2, v3, v4, v5, v6
    v1 = input("Figura prvog igrača (Default = ○): ")
    v4 = input("Dama prvog igrača (Default = ⬤): ")
    v2 = input("Figura drugog igrača (Default = ⬛): ")
    v5 = input("Dama drugog igrača (Default = □): ")
    v3 = input("Polje prethodng položaja (Default = ░): ")
    v6 = input("Polje pojedenoe figure (Default = －): ")

    v1 = "○" if v1 == "" else v1
    v2 = "⬤" if v2 == "" else v2
    v3 = "░" if v3 == "" else v3
    v4 = "□" if v4 == "" else v4
    v5 = "⬛" if v5 == "" else v5
    v6 = "－" if v6 == "" else v6


# if j == 0: j = " "
# if j == 1: j = "○"
# if j == 2: j = "⬤"
# if j == 3: j = "░"
# if j == 4: j = "□"
# if j == 5: j = "⬛"
# if j == 6: j = "－"

v1 = "○"
v2 = "⬤"
v3 = "░"
v4 = "□"
v5 = "⬛"
v6 = "－"
force_jump = False
pc_first = False
status = "NOVA IGRA"
depth = 5
variable_depth = True
turn = 0


def last_jump_to_str(last_jump):
    for lj in last_jump:
        b2 = lj % 10
        lj = int(lj / 10)
        b1 = lj % 10
        lj = int(lj / 10)
        a2 = lj % 10
        lj = int(lj / 10)
        a1 = lj % 10

        print(a1, a2, b1, b2)


def last_jump_to_list(last_jump):
    jumps = []
    for lj in last_jump:
        b2 = lj % 10
        lj = int(lj / 10)
        b1 = lj % 10
        lj = int(lj / 10)
        a2 = lj % 10
        lj = int(lj / 10)
        a1 = lj % 10

        jumps.append([[a1, a2], [b1, b2]])
    return jumps


if __name__ == '__main__':

    while True:
        time_stack = Stack()
        config_print()
        f_jump()
        tabla1 = Board()
        tabla1.play_game()
