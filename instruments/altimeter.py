#!/usr/bin/python3

import sys
import math
from PyQt4 import QtGui,  QtCore

class SerialThread(QtCore.QThread):
    altitudeChanged = QtCore.pyqtSignal(float)

    def __init__(self):
        super(SerialThread, self).__init__()
        self.serial = sys.stdin

    def run(self):
        try:
            altitude = 0.0
            for line in self.serial:
                print(line)
                l = line.strip().split()
                if len(l)!= 5:
                    continue
                altitude = float(l[4])
                self.altitudeChanged.emit(altitude)
        except Exception as e:
            print(e)
            pass

class AltimeterWidget(QtGui.QWidget):
    
    def __init__(self,  altitude=0):
        super(AltimeterWidget, self).__init__()
        self.altitude=altitude
        
        #Define Pens and fonts
        self.thickPen=QtGui.QPen(QtCore.Qt.white,  6,  cap=QtCore.Qt.FlatCap)
        self.mediumPen=QtGui.QPen(QtCore.Qt.white,  4,  cap=QtCore.Qt.FlatCap)
        self.thinPen=QtGui.QPen(QtCore.Qt.white,  2,  cap=QtCore.Qt.FlatCap)
        self.planePen=QtGui.QPen(QtCore.Qt.white, 2, cap=QtCore.Qt.FlatCap)
        
        self.textPen=QtGui.QPen(QtCore.Qt.yellow, 4,  cap=QtCore.Qt.FlatCap)
        self.textFont=QtGui.QFont("Times", 18, 75)
        
        self.textAltPen=QtGui.QPen(QtCore.Qt.white, 2,  cap=QtCore.Qt.FlatCap)
        self.textAltFont=QtGui.QFont("Times", 12, 75)
        
        # Define points for the arrow shapes
        arrow1points=[[0, -160], [10, 0], [0, 10], [-10, 0]]
        arrow2points=[[0, -115], [7, -100], [-7, -100]]
        arrow22points=[[-7, -100], [7, -100], [3, -95], [-3, -95]]
        arrow23points=[[-3, -95], [3, -95], [10, 0], [0, 10], [10, 0]]
        
        #arrow3points=[]
        
        self.arrow1Poly = QtGui.QPolygonF([ QtCore.QPointF(*p) for p in arrow1points] + 
                                         [ QtCore.QPointF(-p[0], p[1]) for p in reversed(arrow1points[1:-1])])
        self.arrow2Poly = QtGui.QPolygonF([ QtCore.QPointF(*p) for p in arrow2points] + 
                                         [ QtCore.QPointF(-p[0], p[1]) for p in reversed(arrow2points[1:-1])])
        self.arrow22Poly = QtGui.QPolygonF([ QtCore.QPointF(*p) for p in arrow22points] + 
                                         [ QtCore.QPointF(-p[0], p[1]) for p in reversed(arrow22points[1:-1])])
        self.arrow23Poly = QtGui.QPolygonF([ QtCore.QPointF(*p) for p in arrow23points] + 
                                         [ QtCore.QPointF(-p[0], p[1]) for p in reversed(arrow23points[1:-1])])

        
        # Setup the user interface
        self.setGeometry(300, 300, 340, 340)
        self.setWindowTitle('Altimeter')
        self.show()
        
    def setAltitude(self,  altitude):
        self.altitude = altitude
        self.update()
    
    def paintEvent(self, e):
        """ Draw the altimeter """
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setRenderHint(QtGui.QPainter.TextAntialiasing)
        qp.translate(170, 170)
        
        qp.save()
        self.drawRing(qp)
        qp.restore()
        
        # Draw altitude
        
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setBrush(QtGui.QColor(0, 0, 0))
        qp.drawRect(120, -15, 40, 30)
        qp.setPen(self.textAltPen)
        qp.setFont(self.textAltFont)
        text=self.altitude
        qp.drawText(155-qp.fontMetrics().width(str(text)), qp.fontMetrics().height()/4, str(text))

        # Draw the arrows
        
        qp.setPen(QtGui.QColor(255, 250, 250))
        qp.setBrush(QtGui.QColor(255, 250, 250))
        
        qp.save()
        qp.rotate(self.altitude*3.6)
        qp.drawPolygon(self.arrow2Poly)
        qp.drawPolygon(self.arrow22Poly)
        qp.drawPolygon(self.arrow23Poly)
        qp.restore()
        
        qp.save()
        qp.rotate(self.altitude*36)
        qp.drawPolygon(self.arrow1Poly)
        qp.restore()
        
    def drawRing(self, qp):
        """ Draw the ring of the altimeter"""
        qp.setPen(QtGui.QColor(104, 104, 104))
        qp.setBrush(QtGui.QColor(0, 0, 0))
        qp.drawEllipse(-170, -170, 340, 340)

        qp.save()
        
        # Draw the lines on the altimeter ring
        for i in range(0, 50):
            angle = i * 7.2
            if i % 5 == 0:
                qp.setPen(self.thickPen)
                qp.drawLine(0, -170, 0, -130)
                qp.setPen(self.textPen)
                qp.setFont(self.textFont)
                
                qp.save()
                qp.translate(0, -115)
                qp.rotate(-angle)
                
                number=str(int(i/5))
                rect=qp.fontMetrics().tightBoundingRect(number)
                qp.drawText(-rect.width()/2, rect.height()/2, number)
                
                qp.restore()
            else:
                qp.setPen(self.mediumPen)
                qp.drawLine(0, -170, 0, -140)
            qp.rotate(7.2)
            
        qp.restore()
        
def main():
    app = QtGui.QApplication(sys.argv)
    altimeter = AltimeterWidget(2.50)
    thread = SerialThread()
    thread.headingChanged.connect(compass.setAltitude)
    thread.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
