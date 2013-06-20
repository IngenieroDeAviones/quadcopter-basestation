#! /usr/bin/env python3

import sys
import math
from PyQt4 import QtGui,  QtCore

class Instrument(QtGui.QWidget):
    layoutEditModeEntered = QtCore.pyqtSignal()
    layoutEditModeExitted = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layoutEdit = False
        self.colSpan = 3
        self.rowSpan = 3


    def setColSpan(self, colSpan):
        self.colSpan = colSpan


    def setRowSpan(self, rowSpan):
        self.rowSpan = rowSpan


    def setSpan(self, colSpan, rowSpan=None):
        self.setColSpan(colSpan)
        self.setRowSpan(rowSpan if not rowSpan is None else colSpan)


    def enterLayoutEditMode(self):
        self.layoutEdit = True
        self.layoutEditModeEntered.emit()


    def exitLayoutEditMode(self):
        self.layoutEdit = False
        self.layoutEditModeExitted.emit()


