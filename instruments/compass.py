#!/usr/bin/python3

import sys
from PyQt4 import QtGui,  QtCore


class SerialThread(QtCore.QThread):
    headingChanged = QtCore.pyqtSignal(float)

    def __init__(self):
        super(SerialThread, self).__init__()
        self.serial = sys.stdin

    def run(self):
        try:
            heading = 0
            for line in self.serial:
                l = line.strip().split()
                if l[0] != "T:" or len(l) != 18:
                    continue
                if heading != float(l[10]):
                    heading = float(l[10])
                    print(heading)
                    self.headingChanged.emit(heading)
        except Exception as e:
            print(e)


class CompassWidget(QtGui.QWidget):
    
    def __init__(self,  heading=0):
        super(CompassWidget, self).__init__()
        
        self.heading=heading
        
        #Define Lines
        self.thick=QtGui.QPen(QtCore.Qt.white,  6,  cap=QtCore.Qt.FlatCap)
        self.medium=QtGui.QPen(QtCore.Qt.white,  4,  cap=QtCore.Qt.FlatCap)
        self.thin=QtGui.QPen(QtCore.Qt.white,  2,  cap=QtCore.Qt.FlatCap)
        self.plane=QtGui.QPen(QtCore.Qt.white, 2, cap=QtCore.Qt.FlatCap)
        
        self.text2=QtGui.QPen(QtCore.Qt.yellow, 4,  cap=QtCore.Qt.FlatCap)
        self.text=QtGui.QPen(QtCore.Qt.red, 4,  cap=QtCore.Qt.FlatCap)
        self.textfont=QtGui.QFont("Times", 18, 75)
        
        planepoints=[[0, -100], [0, -85], [5, -75], [8, -40], [75, 5], [75, 20], [7, -5], [5, 40], [25, 60], [25, 70], [3,  58], [0, 62], [-3, 58], [-25, 70], [-25, 60], [-5, 40], [-7, -5], [-75, 20], [-75, 5], [-8, -40], [-5, -75], [0, -85]]
        self.planepoly=self.poly(planepoints)
        
        self.initUI()
        
    def initUI(self):      

        self.setGeometry(300, 300, 340, 340)
        self.setWindowTitle('Compass')
        self.show()
        
    def poly(self, pts):
        return QtGui.QPolygonF(list(map(lambda p: QtCore.QPointF(*p), pts)))

    def setHeading(self, heading):
        self.heading = heading
        self.update()

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        qp.translate(170,  170)
        
        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)
        qp.setBrush(QtGui.QColor(0, 0, 0))
        qp.drawEllipse(-170, -170, 340, 340)
        
        qp.save()

        qp.rotate(self.heading)
        
        rotation = 0
        while rotation < 360:
            
            if rotation % 30 == 0:
                qp.setPen(self.thick)
                qp.drawLine(0, -170, 0, -130)
                
                if rotation == 0:
                    qp.setPen(self.text)
                    qp.setFont(self.textfont)
                    qp.drawText(-qp.fontMetrics().width("N")/2, -110,  "N")
                elif rotation == 90:
                    qp.setPen(self.text)
                    qp.setFont(self.textfont)
                    qp.drawText(-qp.fontMetrics().width("E")/2, -110,  "E")
                elif rotation == 180:
                    qp.setPen(self.text)
                    qp.setFont(self.textfont)
                    qp.drawText(-qp.fontMetrics().width("S")/2, -110,  "S")
                elif rotation == 270:
                    qp.setPen(self.text)
                    qp.setFont(self.textfont)
                    qp.drawText(-qp.fontMetrics().width("W")/2, -110,  "W")
                else:
                    qp.setPen(self.text2)
                    qp.setFont(self.textfont)
                    qp.drawText(-qp.fontMetrics().width(str(int(rotation/10)))/2, -110, str(int(rotation/10)))
            elif rotation % 10 == 0:
                qp.setPen(self.medium)
                qp.drawLine(0, -170, 0, -140)
            elif rotation % 5 == 0:
                qp.setPen(self.thin)
                qp.drawLine(0, -170, 0, -150)
            
            qp.rotate(5)
            rotation += 5

        qp.restore()
        
        # Draw airplane
        qp.setPen(self.plane)
        qp.drawPolyline(self.planepoly)
        
        qp.end()
        
    def drawRectangles(self, qp):
      
        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)
        qp.setBrush(QtGui.QColor(0, 0, 0))
        qp.drawEllipse(-45, -45, 90, 90)
        
        
   
def main():
    
    app = QtGui.QApplication(sys.argv)
    compass = CompassWidget()
    thread = SerialThread()
    thread.headingChanged.connect(compass.setHeading)
    thread.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
