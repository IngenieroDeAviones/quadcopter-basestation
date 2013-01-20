#!/usr/bin/python3

import sys
import math
from PyQt4 import QtGui,  QtCore

#class SerialThread(QtCore.QThread):
#    altitudeChanged = QtCore.pyqtSignal(float)
#
#    def __init__(self):
#        super(SerialThread, self).__init__()
#        self.serial = sys.stdin
#
#    def run(self):
#        try:
#            altitude = 0.0
#            for line in self.serial:
#                print(line)
#                l = line.strip().split()
#                if len(l)!= 5:
#                    continue
#                altitude = float(l[4])
#                self.altitudeChanged.emit(altitude)
#        except Exception as e:
#            print(e)
#            pass

class AltimeterWidget(QtGui.QWidget):
    
    def __init__(self, pitch=0, rotation=0):
        super(AltimeterWidget, self).__init__()
        self.rotation=rotation
        self.pitch=pitch
        
        #Define Pens and fonts
        self.thickPen=QtGui.QPen(QtCore.Qt.white,  6,  cap=QtCore.Qt.FlatCap)
        self.mediumPen=QtGui.QPen(QtCore.Qt.white,  4,  cap=QtCore.Qt.FlatCap)
        self.thinPen=QtGui.QPen(QtCore.Qt.white,  2,  cap=QtCore.Qt.FlatCap)
        self.planePen=QtGui.QPen(QtCore.Qt.white, 2, cap=QtCore.Qt.FlatCap)
        
        self.textPen=QtGui.QPen(QtCore.Qt.yellow, 4,  cap=QtCore.Qt.FlatCap)
        self.textFont=QtGui.QFont("Times", 18, 75)
        
        self.textAltPen=QtGui.QPen(QtCore.Qt.white, 2,  cap=QtCore.Qt.FlatCap)
        self.textAltFont=QtGui.QFont("Times", 12, 75)
        
#        # Define points for the arrow shapes
#        arrow1points=[[0, -160], [10, 0], [0, 10], [-10, 0]]
#        arrow2points=[[0, -115], [7, -100], [-7, -100]]
#        arrow22points=[[-7, -100], [7, -100], [3, -95], [-3, -95]]
#        arrow23points=[[-3, -95], [3, -95], [10, 0], [0, 10], [10, 0]]
#        
#        #arrow3points=[]
#        
#        self.arrow1Poly = QtGui.QPolygonF([ QtCore.QPointF(*p) for p in arrow1points] + 
#                                         [ QtCore.QPointF(-p[0], p[1]) for p in reversed(arrow1points[1:-1])])
#        self.arrow2Poly = QtGui.QPolygonF([ QtCore.QPointF(*p) for p in arrow2points] + 
#                                         [ QtCore.QPointF(-p[0], p[1]) for p in reversed(arrow2points[1:-1])])
#        self.arrow22Poly = QtGui.QPolygonF([ QtCore.QPointF(*p) for p in arrow22points] + 
#                                         [ QtCore.QPointF(-p[0], p[1]) for p in reversed(arrow22points[1:-1])])
#        self.arrow23Poly = QtGui.QPolygonF([ QtCore.QPointF(*p) for p in arrow23points] + 
#                                         [ QtCore.QPointF(-p[0], p[1]) for p in reversed(arrow23points[1:-1])])

        
        # Setup the user interface
        self.setGeometry(300, 300, 340, 340)
        self.setWindowTitle('Horizon')
        self.show()
    
    def setPitch(self, pitch):
        self.pitch=pitch
        self.update()

    def setRotation(self,  rotation):
        self.rotation=rotation
        self.update()
    
    def paintEvent(self, e):
        """ Draw the altimeter """
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setRenderHint(QtGui.QPainter.TextAntialiasing)
        qp.translate(170, 170)
        
        qp.save()
        self.drawPitch(qp)
        qp.restore()
        
    def drawPitch(self, qp):
        
        qp.save()
        qp.rotate(self.rotation)
        qp.save()
        qp.translate(0, self.pitch*16/2.5)
        """ Draw the background"""
        qp.setPen(QtGui.QColor(102, 51, 0))
        qp.setBrush(QtGui.QColor(102, 51, 0))
        qp.drawRect(QtCore.QRectF(-500, 0, 1000, 500))
        qp.setPen(QtGui.QColor(0, 153, 255))
        qp.setBrush(QtGui.QColor(0, 153, 255))
        qp.drawRect(QtCore.QRectF(-500, -500, 1000, 500))
        
        # draw the pitch lines
        
        qp.setPen(self.thinPen)
        qp.setFont(self.textAltFont)
        qp.drawLine(-500, 0, 500, 0)

        y=-18
        for angle in range(-450, 450, 25):
            if angle % 100 == 0:
                qp.drawLine(-80, y*16, 80, y*16)
                if angle != 0:
                    text=str(int(abs(angle)/10))
                    qp.drawText(-90-qp.fontMetrics().width(text), y*16+qp.fontMetrics().height()/4, text)
                    qp.drawText(90, y*16+qp.fontMetrics().height()/4, text)
            elif angle % 50 == 0:
                qp.drawLine(-40, y*16, 40, y*16)
            else:
                qp.setPen(self.thinPen)
                qp.drawLine(-20, y*16, 20, y*16)
            y+=1
        
        qp.restore()
        
        # Draw roll lines
        qp.setPen(QtGui.QColor(0, 153, 255))
        qp.setBrush(QtGui.QColor(0, 153, 255))
        qp.drawRect(QtCore.QRectF(-170, -250, 340, 110))
        
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
        qp.setBrush(QtGui.QColor(255, 255, 255))
        qp.drawPolygon(QtCore.QPointF(0, -160), QtCore.QPointF(math.sqrt(2)*7.5, -145), QtCore.QPointF(-math.sqrt(2)*7.5, -145))
        

def main():
    app = QtGui.QApplication(sys.argv)
    mainWidget = QtGui.QWidget()
    altimeter = AltimeterWidget()
    vscrollbar = QtGui.QScrollBar(QtCore.Qt.Vertical)
    vscrollbar.valueChanged.connect(altimeter.setPitch)
    vscrollbar.setRange(-90, 90)
    hscrollbar = QtGui.QScrollBar(QtCore.Qt.Horizontal)
    hscrollbar.valueChanged.connect(altimeter.setRotation)
    hscrollbar.setRange(-90, 90)
    layout = QtGui.QGridLayout()
    layout.addWidget(altimeter, 0, 0)
    layout.addWidget(hscrollbar, 1, 0)
    layout.addWidget(vscrollbar, 0, 1)
    mainWidget.setLayout(layout)
    mainWidget.setGeometry(300, 300, 360, 360)
    mainWidget.show()
#    thread = SerialThread()
#    thread.headingChanged.connect(compass.setAltitude)
#    thread.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
