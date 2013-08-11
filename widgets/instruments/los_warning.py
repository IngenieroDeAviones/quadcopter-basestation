#!/usr/bin/python3

import sys
from PyQt4 import QtGui, QtCore

import os
sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))] + sys.path
from widgets.instruments import instrument

class LosWarningWidget(instrument.Instrument):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.flashText)
        self.lightOn = False

        #Define pens and fonts
        self.bgPen = QtGui.QPen(QtCore.Qt.black,  2,  cap=QtCore.Qt.FlatCap)

        self.textPenRed = QtGui.QPen(QtCore.Qt.red, 4, cap=QtCore.Qt.FlatCap)
        self.textPenGrey = QtGui.QPen(QtGui.QColor(20, 20, 20), 4, cap=QtCore.Qt.FlatCap)
        self.textFont = QtGui.QFont("Times", 72, 75)

        self.setGeometry (300, 300, 340, 340)
        self.setWindowTitle("LOS Warning")
        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setRenderHint(QtGui.QPainter.TextAntialiasing)

        size=min(self.width()/340, self.height()/340)

        qp.scale(size, size)

        qp.setPen(self.bgPen)
        qp.setBrush(QtGui.QColor(0, 0, 0))

        qp.drawRect(0, 0, 340, 340)

        qp.translate(170, 170)

        qp.setFont(self.textFont)
        if self.lightOn:
            qp.setPen(self.textPenRed)
        else:
            qp.setPen(self.textPenGrey)

        string = "Signal"
        rect = qp.fontMetrics().tightBoundingRect(string)
        qp.drawText(-rect.width()/2, -40, string)

        string = "Lost"
        rect = qp.fontMetrics().tightBoundingRect(string)
        qp.drawText(-rect.width()/2, 60 + rect.height()/2, string)

    def flashText(self):
        self.lightOn = not self.lightOn
        self.update()

    def setAlarm(self, alarmOn=True):
        print("setAlarm")
        if alarmOn:
            self.timer.start(500)
        else:
            self.timer.stop()
            self.lightOn = False

def main():

    app=QtGui.QApplication(sys.argv)
    loswarning = LosWarningWidget()
    loswarning.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
