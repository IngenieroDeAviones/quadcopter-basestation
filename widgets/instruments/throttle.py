#!/usr/bin/python3

import sys
from PyQt4 import QtGui, QtCore

import os
sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))] + sys.path
from widgets.instruments import instrument

class ThrottleWidget(instrument.Instrument):
    valueChanged = QtCore.pyqtSignal(int, int, int, int)
    def __init__(self, parent=None):
        super().__init__()
        self.motor1 = 0
        self.motor2 = 0
        self.motor3 = 0
        self.motor4 = 0

        self.initUI()

    def initUI(self):

        self.sld1 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld2 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld3 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld4 = QtGui.QSlider(QtCore.Qt.Vertical, self)

        self.sld1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld4.setFocusPolicy(QtCore.Qt.NoFocus)

        self.sld1.setRange(0,1000)
        self.sld2.setRange(0,1000)
        self.sld3.setRange(0,1000)
        self.sld4.setRange(0,1000)

        self.sld1.setGeometry(30, 20, 30, 255)
        self.sld2.setGeometry(60, 20, 30, 255)
        self.sld3.setGeometry(90, 20, 30, 255)
        self.sld4.setGeometry(120, 20, 30, 255)

        self.sld1.valueChanged[int].connect(self.changeValue)
        self.sld2.valueChanged[int].connect(self.changeValue)
        self.sld3.valueChanged[int].connect(self.changeValue)
        self.sld4.valueChanged[int].connect(self.changeValue)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Throttle control')
        self.show

    def changeValue(self, value):
        if self.sender() == self.sld1:
            self.motor1 = value
        elif self.sender() == self.sld2:
            self.motor2 = value
        elif self.sender() == self.sld3:
            self.motor3 = value
        elif self.sender() == self.sld4:
            self.motor4 = value

        self.valueChanged.emit(self.motor1, self.motor2, self.motor3, self.motor4)

def main():
    
    app = QtGui.QApplication(sys.argv)
    throttle = ThrottleWidget()
    throttle.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
