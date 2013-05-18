#!/usr/bin/python3

import sys
import math
from PyQt4 import QtGui, QtCore

class CurrentWidget(QtGui.QWidget):
    def __init__(self, sensor=None, maxCurrent=40):
        super(CurrentWidget, self).__init__()
        self.current = 0
        self.sensor = sensor
        self.maxCurrent = maxCurrent

        #Define Pens and fonts
        self.thickPen=QtGui.QPen(QtCore.Qt.white,  6,  cap=QtCore.Qt.FlatCap)
        self.mediumPen=QtGui.QPen(QtCore.Qt.white,  4,  cap=QtCore.Qt.FlatCap)
        self.thinPen=QtGui.QPen(QtCore.Qt.white,  2,  cap=QtCore.Qt.FlatCap)

        self.redPen=QtGui.QPen(QtCore.Qt.red,  4,  cap=QtCore.Qt.FlatCap)
        self.yellowPen=QtGui.QPen(QtCore.Qt.yellow,  4,  cap=QtCore.Qt.FlatCap)

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

    def setCurrent(self, current):
        self.current = current
        self.update()

    def paintEvent(self, e):
        """ Draw the current sensor """
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

        qp.save()

        qp.setFont(self.textFont)
        qp.setPen(QtGui.QColor(255, 255, 255))
        qp.setBrush(QtGui.QColor(255, 255, 255))

        qp.translate(0,-130)
        string = "A"
        rect = qp.fontMetrics().tightBoundingRect(string)
        qp.drawText(-rect.width()/2, rect.height()/2, string)
        qp.restore()

        """ Draw the arrow """
        qp.setPen(QtGui.QColor(220, 51, 0))
        qp.setBrush(QtGui.QColor(220, 51, 0))

        qp.save()
        qp.translate(0,100)
        qp.rotate(-60+2*min(self.current, 60))
        qp.drawPolygon(self.arrow1Poly)
        qp.restore()
        



    def drawRing(self, qp):
        qp.save()
        qp.setFont(self.textFont)
        qp.setBrush(QtGui.QColor(255, 255, 255))

        qp.translate(0, 100)

        """ Draw warning colors """
        qp.setPen(self.redPen)

        rectangle = QtCore.QRect(-172, -172, 344, 344)
        startAngleRed = 30 * 16
        spanAngleRed = (60 - self.maxCurrent) * 2 * 16

        qp.drawArc(rectangle, startAngleRed, spanAngleRed)

        qp.setPen(self.yellowPen)
        startAngleYellow = startAngleRed + spanAngleRed
        spanAngleYellow = 20 * 16

        qp.drawArc(rectangle, startAngleYellow, spanAngleYellow)

        qp.rotate(-60)

        for current in range(0, 61, 5):
            if current % 10 == 0:
                qp.setPen(self.thickPen)
                qp.drawLine(0, -190, 0, -170)
                angle = -60 + 2*current
                qp.save()
                qp.translate(0, -150)
                qp.rotate(-angle)
    
                number = str(current)
                rect=qp.fontMetrics().tightBoundingRect(number)
                qp.drawText(-rect.width()/2, rect.height()/2, number)
                qp.restore()
            else:
                qp.setPen(self.mediumPen)
                qp.drawLine(0, -180, 0, -170)

            qp.rotate(10)

        qp.restore()

def main():

    app=QtGui.QApplication(sys.argv)
    current = CurrentWidget()
    current.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
