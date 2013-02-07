#!/usr/bin/python3

import sys
import math
from PyQt4 import QtGui,  QtCore



class CompassWidget(QtGui.QWidget):
    
    def __init__(self,  heading=0):
        super(CompassWidget, self).__init__()
        self.heading=heading
        
        #Define Pens and fonts
        self.thickPen=QtGui.QPen(QtCore.Qt.white,  6,  cap=QtCore.Qt.FlatCap)
        self.mediumPen=QtGui.QPen(QtCore.Qt.white,  4,  cap=QtCore.Qt.FlatCap)
        self.thinPen=QtGui.QPen(QtCore.Qt.white,  2,  cap=QtCore.Qt.FlatCap)
        self.planePen=QtGui.QPen(QtCore.Qt.white, 2, cap=QtCore.Qt.FlatCap)
        
        self.numbersPen=QtGui.QPen(QtCore.Qt.yellow, 4,  cap=QtCore.Qt.FlatCap)
        self.textPen=QtGui.QPen(QtCore.Qt.red, 4,  cap=QtCore.Qt.FlatCap)
        self.textFont=QtGui.QFont("Times", 18, 75)
        
        # Define points for the airplane shape
        planepoints=[[0, -100], [0, -85], [5, -75], [8, -40], [75, 5], [75, 20], [7, -5], [5, 40], [25, 60], [25, 70], [3,  58], [0, 62]]
        self.planePoly = QtGui.QPolygonF([ QtCore.QPointF(*p) for p in planepoints] + 
                                         [ QtCore.QPointF(-p[0], p[1]) for p in reversed(planepoints[1:-1])])
        
        # Setup the user interface
        self.setGeometry(300, 300, 340, 340)
        self.setWindowTitle('Compass')
        self.show()
        

    def setHeading(self, heading):
        """ Set the compass heading. """
        self.heading = heading
        self.update()


    def paintEvent(self, e):
        """ Draw the compass. """
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setRenderHint(QtGui.QPainter.TextAntialiasing)
        qp.translate(170,  170)
        
        # Draw the compass ring.
        qp.save()
        qp.rotate(-self.heading)
        self.drawRing(qp)
        qp.restore()
        
        # Draw the airplane
        qp.setPen(self.planePen)
        qp.drawPolyline(self.planePoly)
        
        qp.end()
        

    def drawRing(self, qp):
        """ Draw the moving ring of the compass."""
        qp.setPen(QtGui.QColor(104, 104, 104))
        qp.setBrush(QtGui.QColor(0, 0, 0))
        qp.drawEllipse(-170, -170, 340, 340)
        
        qp.save()

        # draw the lines on the compass ring
        for angle in range(0, 360, 5):
            if angle % 30 == 0:
                qp.setPen(self.thickPen)
                qp.drawLine(0, -170, 0, -130)
            elif angle % 10 == 0:
                qp.setPen(self.mediumPen)
                qp.drawLine(0, -170, 0, -140)
            else:
                qp.setPen(self.thinPen)
                qp.drawLine(0, -170, 0, -150)
            qp.rotate(5)

        qp.restore()
        qp.save()

        # Draw the compass headings
        qp.setPen(self.textPen)
        qp.setFont(self.textFont)
        for text in ["N", "E", "S", "W"]:
            qp.drawText(-qp.fontMetrics().width(text)/2, -110,  text)
            qp.rotate(90)

        qp.restore()
        qp.save()

        # draw the numbers
        qp.setPen(self.numbersPen)
        qp.setFont(self.textFont)
        for angle in range(0, 360, 30):
            if angle % 90 != 0:
                text = str(int(angle/10))
                qp.drawText(-qp.fontMetrics().width(text)/2, -110, text)
            qp.rotate(30)
            
        qp.restore()


def main():
    import os
    sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))] + sys.path
    import parser

    app = QtGui.QApplication(sys.argv)
    compass = CompassWidget()
    thread = parser.ParserThread(open('/dev/arduino'))
    sensorParser = parser.SensorDataParser(thread)
    sensorParser.magnetometerData.connect(lambda x, y, z, h: compass.setHeading(h))
    thread.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
