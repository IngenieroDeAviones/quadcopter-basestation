#! /usr/bin/env python3

import sys
import math
from PyQt4 import QtGui,  QtCore

class Instrument(QObject):
    layoutEditModeEntered = QtCore.pyqtSignal()
    layoutEditModeExitted = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
