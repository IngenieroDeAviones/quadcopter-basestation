#!/usr/bin/python3

import sys
import math
from PyQt4 import QtGui,  QtCore

import os
sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))] + sys.path
from widgets.instruments import instrument
from processing import filters


class HorizonWidget(instrument.Instrument):
    roll = 0
    pitch = 0
    
    def __init__(self, estimator=None, parent=None):
        super(HorizonWidget, self).__init__(parent)

        self.estimator = estimator
        if estimator:
            self.rotation = filters.LowPass(self.estimator.rotation, 10)
            self.rotation.updated.connect(self.updateRotation)

        # Define Pens and fonts
        self.thickPen=QtGui.QPen(QtCore.Qt.white,  6,  cap=QtCore.Qt.FlatCap)
        self.mediumPen=QtGui.QPen(QtCore.Qt.white,  4,  cap=QtCore.Qt.FlatCap)
        self.thinPen=QtGui.QPen(QtCore.Qt.white,  2,  cap=QtCore.Qt.FlatCap)
        self.planePen=QtGui.QPen(QtCore.Qt.white, 2, cap=QtCore.Qt.FlatCap)
        
        self.textPen=QtGui.QPen(QtCore.Qt.yellow, 4,  cap=QtCore.Qt.FlatCap)
        self.textFont=QtGui.QFont("Times", 18, 75)
        
        self.textAltPen=QtGui.QPen(QtCore.Qt.white, 2,  cap=QtCore.Qt.FlatCap)
        self.textAltFont=QtGui.QFont("Times", 12, 75)
        
        # Setup the user interface
        self.setGeometry(300, 300, 340, 340)
        self.setWindowTitle('Horizon')
    
    def setPitch(self, pitch):
        self.pitch=pitch
        self.update()

    def setRoll(self, roll):
        self.roll=roll
        self.update()
    
    def paintEvent(self, e):
        """ Draw the horizon """
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setRenderHint(QtGui.QPainter.TextAntialiasing)

        size=min(self.width()/340, self.height()/340)

        qp.scale(size, size)
        qp.translate(170, 170)
        
        qp.save()
        self.draw(qp)
        qp.restore()
        
    def draw(self, qp):
        
        qp.save()
        qp.rotate(self.roll)
        qp.save()
        qp.translate(0, self.pitch*16/2.5)
        # Draw the background
        qp.setPen(QtGui.QColor(102, 51, 0))
        qp.setBrush(QtGui.QColor(102, 51, 0))
        qp.drawRect(QtCore.QRectF(-5000, 0, 10000, 5000))
        qp.setPen(QtGui.QColor(0, 153, 255))
        qp.setBrush(QtGui.QColor(0, 153, 255))
        qp.drawRect(QtCore.QRectF(-5000, -5000, 10000, 5000))
        
        # draw the pitch lines
        
        qp.setPen(self.thinPen)
        qp.setFont(self.textAltFont)
        qp.drawLine(-500, 0, 500, 0)

        y=-18
        for angle in range(-450, 450, 25):
            if angle % 100 == 0 and y * 16 > -140 - self.pitch * 16 / 2.5:
                qp.drawLine(-80, y*16, 80, y*16)
                if angle != 0:
                    text=str(int(abs(angle)/10))
                    qp.drawText(-90-qp.fontMetrics().width(text), y*16+qp.fontMetrics().height()/4, text)
                    qp.drawText(90, y*16+qp.fontMetrics().height()/4, text)
            elif angle % 50 == 0 and y * 16 > -140 - self.pitch * 16 / 2.5:
                qp.drawLine(-40, y*16, 40, y*16)
            elif y * 16 > -140 - self.pitch * 16 / 2.5:
                qp.setPen(self.thinPen)
                qp.drawLine(-20, y*16, 20, y*16)
            y+=1
        
        qp.restore()
        
        # Draw roll lines
        qp.setPen(self.thinPen)
        qp.setFont(self.textAltFont)
        qp.setBrush(QtGui.QColor(255, 255, 255))
        
        qp.save()
        
        qp.rotate(-60)
        
        
        for angle in range (0, 121, 30):
            qp.drawLine(0, -170, 0, -160)
            qp.rotate(30)
        
        qp.restore()
        
        angles=[10, 20, 45]
        
        for angle in angles+[-angle for angle in angles]:
            qp.save()
            qp.rotate(angle)
            qp.drawLine(0, -165, 0, -160)
            qp.restore()
        
        qp.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        qp.drawPolygon(QtCore.QPointF(-math.sqrt(2)*5, -170), QtCore.QPointF(math.sqrt(2)*5, -170), QtCore.QPointF(0, -160))
        qp.restore()
        
        qp.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        qp.setBrush(QtGui.QColor(255, 102, 0))        
        qp.drawPolygon(QtCore.QPointF(0, -160), QtCore.QPointF(math.sqrt(2)*7.5, -145), QtCore.QPointF(-math.sqrt(2)*7.5, -145))

        qp.setPen(QtGui.QPen(QtGui.QColor(255, 102, 0), 6))
        qp.drawLine(-100, 0, -30, 0)
        qp.drawLine(-0.5, 0, 0.5, 0)
        qp.drawLine(30, 0, 100, 0)


    def updateRotation(self, stream):
        self.setRoll(math.degrees(stream['roll']))
        self.setPitch(math.degrees(stream['pitch']))
    
def main():
    import os
    sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))] + sys.path
    from processing import estimator
    
    app = QtGui.QApplication(sys.argv)
    horizon = HorizonWidget(estimator.Estimator())
    horizon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
