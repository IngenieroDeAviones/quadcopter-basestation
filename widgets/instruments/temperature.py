#!/usr/bin/python3

import sys
import math
from PyQt4 import QtGui, QtCore

import os
sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))] + sys.path
from widgets.instruments import instrument


class TemperatureWidget(instrument.Instrument):
    def __init__(self, sensor=None, minTemp=120, maxTemp=40, highThreshold=70, criticalThreshold=60, stepSize=10, valueFactor=2, parent=None):
        super().__init__(parent)
        self.temperature = 85
        self.sensor = sensor
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        self.highThreshold = highThreshold
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

        qp.save()

        qp.setFont(self.textFont)
        qp.setPen(QtGui.QColor(255, 255, 255))
        qp.setBrush(QtGui.QColor(255, 255, 255))

        qp.translate(0,-130)
        string = "°C"
        rect = qp.fontMetrics().tightBoundingRect(string)
        qp.drawText(-rect.width()/2, rect.height()/2, string)
        qp.restore()

        """ Draw the temperature symbol """

        qp.save()
        qp.setPen(QtGui.QColor(255, 255, 255))
        qp.setBrush(QtGui.QColor(255, 255, 255))
        if self.minTemp < self.maxTemp:
            if self.temperature >= self.criticalThreshold:
                color = QtCore.Qt.red
            elif self.temperature >= self.highThreshold:
                color = QtCore.Qt.yellow
            else:
                color = QtCore.Qt.white
        else:
            if self.temperature <= self.criticalThreshold:
                color = QtCore.Qt.red
            elif self.temperature <= self.highThreshold:
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

        """ Draw the arrow """
        qp.setPen(QtGui.QColor(220, 51, 0))
        qp.setBrush(QtGui.QColor(220, 51, 0))

        qp.save()
        qp.translate(0,100)
        #qp.rotate(-100+100/(self.maxTemp - self.minTemp)*min(max(self.temperature, 30), 130))
        qp.rotate(min(max(-50 + 100 / (self.maxTemp - self.minTemp)*(self.temperature - self.minTemp), -60), 60))
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
        
        if self.highThreshold < self.criticalThreshold or self.maxTemp < self.minTemp:
            startAngleRed = 40 * 16
            spanAngleRed = (self.maxTemp - self.criticalThreshold) * 100/(self.maxTemp - self.minTemp) * 16

            qp.drawArc(rectangle, startAngleRed, spanAngleRed)

            qp.setPen(self.yellowPen)
            startAngleYellow = startAngleRed + spanAngleRed
            spanAngleYellow = 100/(self.maxTemp - self.minTemp) * (self.criticalThreshold - self.highThreshold) * 16

            qp.drawArc(rectangle, startAngleYellow, spanAngleYellow)

        else:
            startAngleRed = 140 * 16
            spanAngleRed = (self.criticalThreshold - self.minTemp) * 100/(self.maxTemp - self.minTemp) * -16

            qp.drawArc(rectangle, startAngleRed, spanAngleRed)

            qp.setPen(self.yellowPen)
            startAngleYellow = startAngleRed + spanAngleRed
            spanAngleYellow = 100/(self.maxTemp - self.minTemp) * (self.highThreshold - self.criticalThreshold) * -16

            qp.drawArc(rectangle, startAngleYellow, spanAngleYellow)

        qp.rotate(-50)

        if self.minTemp < self.maxTemp:
            for temperature in range(self.minTemp, self.maxTemp+1, self.stepSize):
                if temperature % (self.stepSize * self.valueFactor) == 0:
                    qp.setPen(self.thickPen)
                    qp.drawLine(0, -190, 0, -170)
                    angle = -50 + 100/(self.maxTemp - self.minTemp)*(temperature - self.minTemp)
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

                qp.rotate(100/(self.maxTemp - self.minTemp) * self.stepSize) #2.5)

        else:
            for temperature in reversed(range(self.maxTemp, self.minTemp+1, self.stepSize)):
                if temperature % (self.stepSize * self.valueFactor) == 0:
                    qp.setPen(self.thickPen)
                    qp.drawLine(0, -190, 0, -170)
                    angle = -50 + 100/(self.maxTemp - self.minTemp)*(temperature - self.minTemp)
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

                qp.rotate(100/(self.minTemp - self.maxTemp) * self.stepSize)
        qp.restore()

def main():

    app=QtGui.QApplication(sys.argv)
    thermometer = TemperatureWidget()
    thermometer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
