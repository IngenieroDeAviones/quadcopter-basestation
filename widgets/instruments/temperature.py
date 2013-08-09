#!/usr/bin/python3

import sys
import math
import operator
import numpy as np
from PyQt4 import QtGui, QtCore

import os
sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))] + sys.path
from widgets.instruments import instrument


class GaugeWidget(instrument.Instrument):
    def __init__(self, sensor=None, type="voltage", valueLeft=2.5, valueRight=4.5, warningThreshold=3.2, criticalThreshold=3.0, stepSize=0.1, valueFactor=5, parent=None):
        super().__init__(parent)
        self.value = 3.5
        self.sensor = sensor
        self.type = type
        self.valueLeft = valueLeft
        self.valueRight = valueRight
        self.warningThreshold = warningThreshold
        self.criticalThreshold = criticalThreshold
        self.stepSize = stepSize
        self.valueFactor = valueFactor

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
        if self.type == "temperature":
            self.setWindowTitle('Temperature')
        elif self.type == "current":
            self.setWindowTitle('Current')
        elif self.type == "voltage":
            self.setWindowTitle('Voltage')
        else:
            self.setWindowTitle('Error')
        self.show()

    def setValue(self, value):
        self.value = value
        self.update()

    def paintEvent(self, e):
        """ Draw the gauge """
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
        if self.type == "temperature":
            string = "°C"
        elif self.type == "current":
            string = "A"
        elif self.type == "voltage":
            string = "V"

        rect = qp.fontMetrics().tightBoundingRect(string)
        qp.drawText(-rect.width()/2, rect.height()/2, string)
        qp.restore()

        if self.type == "temperature":
            """ Draw the temperature symbol """
    
            qp.save()
            qp.setPen(QtGui.QColor(255, 255, 255))
            qp.setBrush(QtGui.QColor(255, 255, 255))
            if self.criticalThreshold > self.warningThreshold:
                if self.value >= self.criticalThreshold:
                    color = QtCore.Qt.red
                elif self.value >= self.warningThreshold:
                    color = QtCore.Qt.yellow
                else:
                    color = QtCore.Qt.white
            else:
                if self.value <= self.criticalThreshold:
                    color = QtCore.Qt.red
                elif self.value <= self.warningThreshold:
                    color = QtCore.Qt.yellow
                else:
                    color = QtCore.Qt.white
    
            qp.setPen(QtGui.QPen(color, 5, cap=QtCore.Qt.RoundCap))
            qp.translate(0,50)
            qp.drawEllipse(-3, -3, 6, 6)
            qp.drawLine(0, 0, 0, -40)
            qp.setPen(QtGui.QPen(color, 4, cap=QtCore.Qt.RoundCap))
    
            qp.translate(0,-15)
            qp.drawLine(0, 0, 12, 0)
    
            qp.translate(0,-8)
            qp.drawLine(0, 0, 12, 0)
    
            qp.translate(0,-8)
            qp.drawLine(0, 0, 12, 0)
    
            qp.restore()

        elif self.type == "voltage":
            """ Draw the DC Symbol """

            qp.save()
            #qp.setPen(self.thickPen)
            if self.criticalThreshold > self.warningThreshold:
                if self.value >= self.criticalThreshold:
                    color = QtCore.Qt.red
                elif self.value >= self.warningThreshold:
                    color = QtCore.Qt.yellow
                else:
                    color = QtCore.Qt.white
            else:
                if self.value <= self.criticalThreshold:
                    color = QtCore.Qt.red
                elif self.value <= self.warningThreshold:
                    color = QtCore.Qt.yellow
                else:
                    color = QtCore.Qt.white

            qp.setPen(QtGui.QPen(color, 5))

            qp.translate(0, 10)
            qp.drawLine(-20, 0, 20, 0)

            qp.translate(0, 15)
            qp.drawLine(-20, 0, -12, 0)
            qp.drawLine(-4, 0, 4, 0)
            qp.drawLine(12, 0, 20, 0)

            qp.restore()

        """ Draw the arrow """
        qp.setPen(QtGui.QColor(220, 51, 0))
        qp.setBrush(QtGui.QColor(220, 51, 0))

        qp.save()
        qp.translate(0,100)
        qp.rotate(min(max(-50 + 100 / (self.valueRight - self.valueLeft)*(self.value - self.valueLeft), -60), 60))
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
        
        if operator.xor(self.warningThreshold < self.criticalThreshold, self.valueRight < self.valueLeft):
            # Arc angle is give in 1/16th of a degree. Therefore 40 * 16 in startAngleRed is 40 degrees
            startAngleRed = 40 * 16
            spanAngleRed = (self.valueRight - self.criticalThreshold) * 100/(self.valueRight - self.valueLeft) * 16

            qp.drawArc(rectangle, startAngleRed, spanAngleRed)

            qp.setPen(self.yellowPen)
            startAngleYellow = startAngleRed + spanAngleRed
            spanAngleYellow = 100/(self.valueRight - self.valueLeft) * (self.criticalThreshold - self.warningThreshold) * 16

            qp.drawArc(rectangle, startAngleYellow, spanAngleYellow)

        else:
            startAngleRed = 140 * 16
            spanAngleRed = (self.criticalThreshold - self.valueLeft) * 100/(self.valueRight - self.valueLeft) * -16

            qp.drawArc(rectangle, startAngleRed, spanAngleRed)

            qp.setPen(self.yellowPen)
            startAngleYellow = startAngleRed + spanAngleRed
            spanAngleYellow = 100/(self.valueRight - self.valueLeft) * (self.warningThreshold - self.criticalThreshold) * -16

            qp.drawArc(rectangle, startAngleYellow, spanAngleYellow)

        qp.rotate(-50)

        if self.valueLeft < self.valueRight:
            calc = self.valueRight - self.valueLeft
        else:
            calc = self.valueLeft - self.valueRight

        step = (abs(self.valueLeft - self.valueRight) / self.stepSize) + 1
        isint = type(self.valueLeft) == int and type(self.valueRight) == int and type(self.stepSize) == int

        for value in np.linspace(self.valueLeft, self.valueRight, step):
            if value % (self.stepSize * self.valueFactor) == 0:
                qp.setPen(self.thickPen)
                qp.drawLine(0, -190, 0, -170)
                angle = -50 + 100/(self.valueRight - self.valueLeft)*(value - self.valueLeft)
                qp.save()
                qp.translate(0, -150)
                qp.rotate(-angle)

                number = str(value if not isint else int(value))
                rect=qp.fontMetrics().tightBoundingRect(number)
                qp.drawText(-rect.width()/2, rect.height()/2, number)
                qp.restore()
            else:
                qp.setPen(self.mediumPen)
                qp.drawLine(0, -180, 0, -170)

            qp.rotate(100 / calc * self.stepSize)

        qp.restore()

def main():

    app=QtGui.QApplication(sys.argv)
    gauge = GaugeWidget()
    gauge.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
