#!/usr/bin/python3

import sys
import math
from PyQt4 import QtGui, QtCore

class TemperatureWidget(QtGui.QWidget):
    def __init__(self, sensor=None):
        super(TemperatureWidget, self).__init__()
        self.temperature = 0
        self.sensor = sensor

        #Define Pens and fonts
        self.thickPen=QtGui.QPen(QtCore.Qt.white,  6,  cap=QtCore.Qt.FlatCap)
        self.mediumPen=QtGui.QPen(QtCore.Qt.white,  4,  cap=QtCore.Qt.FlatCap)
        self.thinPen=QtGui.QPen(QtCore.Qt.white,  2,  cap=QtCore.Qt.FlatCap)

        self.textPen=QtGui.QPen(QtCore.Qt.yellow, 4,  cap=QtCore.Qt.FlatCap)
        self.textFont=QtGui.QFont("Times", 18, 75)

        self.textAltPen=QtGui.QPen(QtCore.Qt.white, 2,  cap=QtCore.Qt.FlatCap)
        self.textAltFont=QtGui.QFont("Times", 12, 75)

        #Define points for the arrow shape
        arrow1points=[[0, -180], [10, 0], [0, 10]]

        self.arrow1Poly = QtGui.QPolygonF([ QtCore.QPointF(*p) for p in arrow1points] +
                                         [ QtCore.QPointF(-p[0], p[1]) for p in reversed(arrow1points[1:-1])])

        #Setup the user interface
        self.setGeometry(300, 300, 340, 340)
        self.setWindowTitle('Temperature')
        self.show()

    def setTemperature(self, temperature):
        self.temperature = temperature
        self.update()

    def paintEvent(self, e):
        """ Draw the temperature sensor """
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setRenderHint(QtGui.QPainter.TextAntialiasing)

        size=min(self.width()/340, self.height()/340)

        qp.scale(size, size)
        qp.translate(170,170)

        qp.save()
        """ Draw the background """
        qp.setPen(QtGui.QColor(104, 104, 104))
        qp.setBrush(QtGui.QColor(0, 0, 0))
        qp.drawEllipse(-170, -170, 340, 340)

        qp.restore()

        self.drawRing(qp)

        qp.setPen(QtGui.QColor(220, 51, 0))
        qp.setBrush(QtGui.QColor(220, 51, 0))

        qp.save()
        qp.translate(0,100)
        qp.rotate(-100+100/80*min(max(self.temperature, 30), 130))
        qp.drawPolygon(self.arrow1Poly)
        qp.restore()
        



    def drawRing(self, qp):
        qp.save()
        qp.setFont(self.textFont)
        qp.setBrush(QtGui.QColor(255, 255, 255))

        qp.translate(0, 100)
        qp.rotate(-50)

        for temperature in range(40, 121, 10):
            if temperature % 20 == 0:
                qp.setPen(self.thickPen)
                qp.drawLine(0, -190, 0, -170)
                angle = -100 + 100/80*temperature
                qp.save()
                qp.translate(0, -150)
                qp.rotate(-angle)
    
                number = str(temperature)
                rect=qp.fontMetrics().tightBoundingRect(number)
                qp.drawText(-rect.width()/2, rect.height()/2, number)
                qp.restore()
            else:
                qp.setPen(self.mediumPen)
                qp.drawLine(0, -180, 0, -170)

            qp.rotate(12.5)

        qp.restore()

def main():

    app=QtGui.QApplication(sys.argv)
    thermometer = TemperatureWidget()
    thermometer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
