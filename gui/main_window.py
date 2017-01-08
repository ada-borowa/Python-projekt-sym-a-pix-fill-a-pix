#!/usr/bin/env python3
""" Main window of Sym-a-pix and Fill-a-pix solver/generator program.
"""
import random

import math
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
import sys

from symapix.imageops.reader import SymAPixReader
from symapix.solver.solver import SymAPixSolver
from fillapix.imageops.reader import FillAPixReader
from fillapix.solver.solver import FillAPixSolver

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'

SIZE = 800
SQUARE = 30
EPS = 5


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        """Initialization of class."""
        super(MainWindow, self).__init__()
        self.status_bar = self.statusBar()
        self.l = QtGui.QVBoxLayout()
        self.content = QtGui.QVBoxLayout()

        self.button_part = QtGui.QHBoxLayout()
        self.curr_game_label = QtGui.QLabel('Currently playing: no game')
        self.curr_game = 0
        self.solve_btn = QtGui.QPushButton('Solve')
        self.clear_btn = QtGui.QPushButton('Clear')
        self.check_btn = QtGui.QPushButton('Check')

        self.puzzle_part = QtGui.QVBoxLayout()
        self.painter = QtGui.QPainter()
        self.board = QtGui.QLabel()
        self.pix_map = QtGui.QPixmap(SIZE, SIZE)

        self.puzzle = None
        self.solver = None
        self.vertical_lines = 0
        self.horizontal_lines = 0
        self.game_size = []

        self.init_gui()

    def init_gui(self):
        """Initialization of UI."""

        # Window setup
        self.setWindowTitle('Puzzles')
        self.resize(SIZE, SIZE + 100)
        cw = QtGui.QWidget()
        self.setCentralWidget(cw)
        cw.setLayout(self.l)

        # Menu setup
        # Sym-a-pix actions
        load_sym = QtGui.QAction('Load puzzle', self)
        load_sym.setStatusTip('Sym-a-pix: Load puzzle from file.')
        load_sym.triggered.connect(self.load_sym_from_file)

        gen_sym = QtGui.QAction('Generate puzzle', self)
        gen_sym.setStatusTip('Sym-a-pix: Generate random puzzle.')
        gen_sym.triggered.connect(self.generate_sym)

        # Fill-a-pix actions
        load_fill = QtGui.QAction('Load puzzle', self)
        load_fill.setStatusTip('Fill-a-pix: Load puzzle from file.')
        load_fill.triggered.connect(self.load_fill_from_file)

        gen_fill = QtGui.QAction('Generate puzzle', self)
        gen_fill.setStatusTip('Fill-a-pix: Generate random puzzle.')
        gen_fill.triggered.connect(self.generate_fill)

        menu_bar = self.menuBar()
        sym_menu = menu_bar.addMenu('&Sym-a-pix')
        sym_menu.addAction(load_sym)
        sym_menu.addAction(gen_sym)

        fill_menu = menu_bar.addMenu('&Fill-a-pix')
        fill_menu.addAction(load_fill)
        fill_menu.addAction(gen_fill)

        # Window's content setup
        self.content.addWidget(self.curr_game_label)
        # Canvas
        self.pix_map.fill(Qt.white)

        self.board.setPixmap(self.pix_map)
        self.board.setMouseTracking(True)
        self.puzzle_part.addWidget(self.board)
        self.content.addLayout(self.puzzle_part)
        # Buttons
        self.solve_btn.clicked.connect(self.solve_game)
        self.clear_btn.clicked.connect(self.clear_game)
        self.check_btn.clicked.connect(self.check_game)
        self.button_part.addWidget(self.solve_btn)
        self.button_part.addWidget(self.clear_btn)
        self.button_part.addWidget(self.check_btn)
        self.button_part.setAlignment(Qt.AlignTop)
        self.content.addLayout(self.button_part)

        self.l.addLayout(self.content)
        self.show()

    def load_sym_from_file(self):
        """Loads sym-a-pix puzzle from file."""
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Zapisz plik', '.')
        try:
            self.change_curr_game(1)
            reader = SymAPixReader(file_name)
            self.puzzle = reader.create_puzzle()
            self.horizontal_lines, self.vertical_lines = reader.get_lines()
            self.solver = SymAPixSolver(self.puzzle)
            self.game_size = self.solver.size
            self.solver.solve()
            self.draw_game()
            self.status_bar.showMessage('Loaded puzzle from file: {}'.format(file_name.split('/')[-1]))
        except IOError:
            self.status_bar.showMessage('Cannot read file: {}'.format(file_name.split('/')[-1]))

    def generate_sym(self):
        print('Sym: Generating random.')

    def load_fill_from_file(self):
        """Loads fill-a-pix puzzle from file."""
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Zapisz plik', '.')
        try:
            self.change_curr_game(2)
            reader = FillAPixReader(file_name)
            self.puzzle = reader.create_puzzle()
            self.horizontal_lines, self.vertical_lines = reader.get_lines()
            self.solver = FillAPixSolver(self.puzzle)
            self.game_size = self.solver.size
            self.solver.solve()
            self.draw_game()
            self.status_bar.showMessage('Loaded puzzle from file: {}'.format(file_name.split('/')[-1]))
        except IOError:
            self.status_bar.showMessage('Cannot read file: {}'.format(file_name.split('/')[-1]))

    def generate_fill(self):
        print('Fill: Generating random.')

    def change_curr_game(self, game):
        """Sets value of label with current game."""
        self.curr_game = game
        if self.curr_game == 0:
            self.curr_game_label.setText('Currently playing: no game')
        elif self.curr_game == 1:
            self.curr_game_label.setText('Currently playing: Sym-a-pix')
        elif self.curr_game == 2:
            self.curr_game_label.setText('Currently playing: Fill-a-pix')

    def mousePressEvent(self, event):
        if self.curr_game == 1:
            x, y = self.get_painter_pos(event.x(), event.y())
            # print(x, y)
            if x % SQUARE < EPS:
                self.change_line(int((x - x % SQUARE) / SQUARE * 2 - 1), int((y - y % SQUARE) / SQUARE * 2))
            elif SQUARE - EPS < x % SQUARE:
                self.change_line(int((x - x % SQUARE + SQUARE) / SQUARE * 2 - 1), int((y - y % SQUARE) / SQUARE * 2))
            elif y % SQUARE < EPS:
                self.change_line(int((x - x % SQUARE) / SQUARE * 2), int((y - y % SQUARE) / SQUARE * 2 - 1))
            elif SQUARE - EPS < y % SQUARE:
                self.change_line(int((x - x % SQUARE) / SQUARE * 2), int((y - y % SQUARE + SQUARE) / SQUARE * 2 - 1))
            self.draw_game()

        elif self.curr_game == 2:
            x, y = self.get_painter_pos(event.x(), event.y())
            if 0 <= x < self.vertical_lines - 1 and 0 <= y < self.horizontal_lines - 1:
                self.change_square(x, y)
                self.draw_game()

        self.check_solved()

    def get_painter_pos(self, i, j):
        """Given position of mouse click, returns clicked square position."""
        i = (i - 5) * ((self.vertical_lines + 1) * SQUARE) / 800
        j = (j - 55) * ((self.horizontal_lines + 1) * SQUARE) / 800
        if self.curr_game == 1:
            if i > SQUARE and j > SQUARE:
                return i - SQUARE, j - SQUARE
            else:
                return -1, -1

        elif self.curr_game == 2:
            if i > SQUARE and j > SQUARE:
                return int((i - SQUARE) / SQUARE), int((j - SQUARE) / SQUARE)
            else:
                return -1, -1

    def draw_game(self):
        """Chooses what to draw."""
        self.draw_lines()
        if self.curr_game == 1:
            self.draw_sym()
        elif self.curr_game == 2:
            self.draw_fill()

    def draw_sym(self):
        """Draws sym-a-pix game."""
        self.draw_solution_lines()
        # self.draw_squares_sym()
        self.draw_circles()

    def draw_fill(self):
        """Draws fill-a-pix game."""
        self.draw_squares_fill()
        self.draw_numbers()

    def draw_lines(self):
        self.pix_map.fill(Qt.white)
        self.painter.begin(self.pix_map)
        self.painter.setWindow(0, 0, (self.vertical_lines + 1) * SQUARE, (self.horizontal_lines + 1) * SQUARE)
        for line in range(1, self.horizontal_lines + 1):
            if line in [1, self.horizontal_lines] and self.curr_game == 1:
                pen = QtGui.QPen()
                pen.setColor(Qt.black)
                pen.setWidth(3)
                self.painter.setPen(pen)
            elif self.curr_game == 2:
                self.painter.setPen(Qt.black)
            else:
                self.painter.setPen(Qt.lightGray)
            self.painter.drawLine(SQUARE, line * SQUARE, self.vertical_lines * SQUARE, line * SQUARE)
        for line in range(1, self.vertical_lines + 1):
            if line in [1, self.vertical_lines] and self.curr_game == 1:
                pen = QtGui.QPen()
                pen.setColor(Qt.black)
                pen.setWidth(3)
                self.painter.setPen(pen)
            elif self.curr_game == 2:
                self.painter.setPen(Qt.black)
            else:
                self.painter.setPen(Qt.lightGray)
            self.painter.drawLine(line * SQUARE, SQUARE, line * SQUARE, self.horizontal_lines * SQUARE)
        self.painter.end()
        self.board.setPixmap(self.pix_map)

    def draw_solution_lines(self):
        curr_user_solution = self.solver.get_user_solution()
        self.painter.begin(self.pix_map)
        self.painter.setWindow(0, 0, (self.vertical_lines + 1) * SQUARE, (self.horizontal_lines + 1) * SQUARE)
        pen = QtGui.QPen()
        pen.setColor(Qt.black)
        pen.setWidth(3)
        self.painter.setPen(pen)
        for i, row in enumerate(curr_user_solution):
            for j, el in enumerate(row):
                if curr_user_solution[i, j] == 1:
                    if i % 2 == 0:
                        self.painter.drawLine(SQUARE * (i/2 + 1), SQUARE * (j/2+1.5), SQUARE * (i/2 + 2), SQUARE * (j/2+1.5))
                    elif j % 2 == 0:
                        self.painter.drawLine(SQUARE * (i/2+1.5), SQUARE * (j/2 + 1), SQUARE * (i/2+1.5), SQUARE * (j/2 + 2))
        self.painter.end()
        self.board.setPixmap(self.pix_map)

    def draw_numbers(self):
        curr_user_solution = self.solver.get_user_solution()
        self.painter.begin(self.pix_map)
        self.painter.setWindow(0, 0, (self.vertical_lines + 1) * SQUARE, (self.horizontal_lines + 1) * SQUARE)
        font = QtGui.QFont('Arial')
        font.setPointSize(22)
        self.painter.setFont(font)
        for i, row in enumerate(self.solver.puzzle):
            for j, el in enumerate(row):
                if el < 100:
                    val = str(int(el))
                    if curr_user_solution[i, j] == 1:
                        self.painter.setPen(Qt.white)
                    else:
                        self.painter.setPen(Qt.black)
                    self.painter.drawText(1.25 * SQUARE + j * SQUARE, 1.85 * SQUARE + i * SQUARE, val)
        self.painter.end()
        self.board.setPixmap(self.pix_map)

    def draw_circles(self):
        """Draws circles in sym-a-pix"""
        colors = self.puzzle.get_colors()
        self.painter.begin(self.pix_map)
        self.painter.setWindow(0, 0, (self.vertical_lines + 1) * SQUARE, (self.horizontal_lines + 1) * SQUARE)
        for i, row in enumerate(self.solver.puzzle):
            for j, el in enumerate(row):
                if el > 0:
                    color = colors[int(el) - 1]
                    self.painter.setBrush(QtGui.QColor(color[2], color[1], color[0]))
                    self.painter.drawEllipse(QtCore.QPoint(SQUARE * 1.5 + SQUARE * j / 2.0,
                                                           SQUARE * 1.5 + SQUARE * i / 2.0), 5, 5)
        self.painter.end()
        self.board.setPixmap(self.pix_map)

    def change_square(self, i, j):
        """Changes color of square and value of user solution in solver."""
        i, j = j, i
        curr_val = self.solver.get_user_value(i, j)
        if curr_val == 1:
            self.solver.set_user_value(i, j, -1)
        else:
            self.solver.set_user_value(i, j, curr_val + 1)

    def change_line(self, i, j):
        self.solver.set_user_value(i, j, (self.solver.get_user_value(i, j) + 1) % 2)

    def draw_squares_sym(self):
        pass

    def draw_squares_fill(self):
        self.painter.begin(self.pix_map)
        self.painter.setWindow(0, 0, (self.vertical_lines + 1) * SQUARE, (self.horizontal_lines + 1) * SQUARE)
        curr_user_solution = self.solver.get_user_solution()
        for i, row in enumerate(curr_user_solution):
            for j, el in enumerate(row):
                if el == -1:
                    self.painter.setBrush(Qt.lightGray)
                elif el == 1:
                    self.painter.setBrush(Qt.black)
                if el != 0:
                    self.painter.drawRect(SQUARE * (j + 1), SQUARE * (i + 1),
                                          SQUARE, SQUARE)
        self.painter.end()
        self.board.setPixmap(self.pix_map)

    def solve_game(self):
        """Gives solution to user."""
        self.solver.set_solved()
        self.draw_game()

    def clear_game(self):
        """Clears game to initial state."""
        self.solver.clear_user_solution()
        self.draw_game()

    def check_game(self):
        """Let's user allow if there are any mistakes."""
        x, y = self.solver.check_user_solution()
        if x > -1 and y > -1:
            self.status_bar.showMessage('You have mistake in: ({}, {})'.format(y + 1, x + 1))
        else:
            self.status_bar.showMessage('Correct!')

    def check_solved(self):
        if self.solver.is_solved_by_user():
            self.painter.begin(self.pix_map)
            self.painter.setWindow(0, 0, (self.vertical_lines + 1) * SQUARE, (self.horizontal_lines + 1) * SQUARE)
            font = QtGui.QFont('Arial')
            font.setPointSize(22)
            self.painter.setFont(font)
            self.painter.setPen(Qt.red)
            self.painter.drawText(SQUARE, SQUARE, 'SOLVED!')
            self.painter.end()
            self.board.setPixmap(self.pix_map)


def main_window():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())