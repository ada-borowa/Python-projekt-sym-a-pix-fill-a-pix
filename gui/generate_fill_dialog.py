#!/usr/bin/env python3
""" Dialog window to choose parameters of fill-a-pix being generated.
"""

from PyQt4 import QtGui

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


class GenerateFillDialog(QtGui.QMainWindow):
    """Dialog window where user can set size of new puzzle"""
    def __init__(self, parent):
        """Initialization of class."""
        super(GenerateFillDialog, self).__init__()
        self.ok_btn = QtGui.QPushButton('OK')
        self.size_value = QtGui.QSpinBox()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Dialog window"""
        self.setWindowTitle('Fill-a-pix: generate game')
        self.resize(200, 120)
        cw = QtGui.QWidget()
        self.setCentralWidget(cw)
        l = QtGui.QGridLayout()
        size_label = QtGui.QLabel('Size: ')

        self.size_value.setMinimum(5)
        self.size_value.setMaximum(20)
        self.size_value.setValue(10)
        l.addWidget(size_label, *(0, 0))
        l.addWidget(self.size_value, *(0, 1))

        self.ok_btn.clicked.connect(self.send_values)
        l.addWidget(self.ok_btn, *(1, 1))
        cw.setLayout(l)

    def send_values(self):
        """Sends user's values to generating function."""
        size = self.size_value.value()
        self.parent.generate_new_fill(size, size)
        self.size_value.setValue(10)
        self.close()
