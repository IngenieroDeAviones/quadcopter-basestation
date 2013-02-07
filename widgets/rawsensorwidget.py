
import sys
from PyQt4 import QtCore, QtGui


class RawSensorWidget(QtGui.QWidget):
    def __init__(self, sensorDataParser):
        super().__init__()
        sensorDataParser.gyroscopeData.connect(self.gyroData)
        sensorDataParser.accelerometerData.connect(self.accelData)
        sensorDataParser.magnetometerData.connect(self.compassData)
        sensorDataParser.barrometerData.connect(self.barroData)

        self.gyroX = QtGui.QLabel()
        self.gyroY = QtGui.QLabel()
        self.gyroZ = QtGui.QLabel()
        self.gyroX.setAlignment(QtCore.Qt.AlignRight)
        self.gyroY.setAlignment(QtCore.Qt.AlignRight)
        self.gyroZ.setAlignment(QtCore.Qt.AlignRight)

        gyroBox = QtGui.QGroupBox('Gyroscope')
        gyroBox.layout = QtGui.QGridLayout()
        gyroBox.layout.addWidget(QtGui.QLabel('x:'), 0, 0)
        gyroBox.layout.addWidget(QtGui.QLabel('y:'), 1, 0)
        gyroBox.layout.addWidget(QtGui.QLabel('z:'), 2, 0)
        gyroBox.layout.addWidget(self.gyroX, 0, 1)
        gyroBox.layout.addWidget(self.gyroY, 1, 1)
        gyroBox.layout.addWidget(self.gyroZ, 2, 1)
        gyroBox.layout.addWidget(QtGui.QLabel('°/s'), 0, 2)
        gyroBox.layout.addWidget(QtGui.QLabel('°/s'), 1, 2)
        gyroBox.layout.addWidget(QtGui.QLabel('°/s'), 2, 2)
        gyroBox.setLayout(gyroBox.layout)

        self.accelX = QtGui.QLabel()
        self.accelY = QtGui.QLabel()
        self.accelZ = QtGui.QLabel()
        self.accelX.setAlignment(QtCore.Qt.AlignRight)
        self.accelY.setAlignment(QtCore.Qt.AlignRight)
        self.accelZ.setAlignment(QtCore.Qt.AlignRight)

        accelBox = QtGui.QGroupBox('Accelerometer')
        accelBox.layout = QtGui.QGridLayout()
        accelBox.layout.addWidget(QtGui.QLabel('x:'), 0, 0)
        accelBox.layout.addWidget(QtGui.QLabel('y:'), 1, 0)
        accelBox.layout.addWidget(QtGui.QLabel('z:'), 2, 0)
        accelBox.layout.addWidget(self.accelX, 0, 1)
        accelBox.layout.addWidget(self.accelY, 1, 1)
        accelBox.layout.addWidget(self.accelZ, 2, 1)
        accelBox.layout.addWidget(QtGui.QLabel('g'), 0, 2)
        accelBox.layout.addWidget(QtGui.QLabel('g'), 1, 2)
        accelBox.layout.addWidget(QtGui.QLabel('g'), 2, 2)
        accelBox.setLayout(accelBox.layout)

        self.compassX = QtGui.QLabel()
        self.compassY = QtGui.QLabel()
        self.compassZ = QtGui.QLabel()
        self.compassX.setAlignment(QtCore.Qt.AlignRight)
        self.compassY.setAlignment(QtCore.Qt.AlignRight)
        self.compassZ.setAlignment(QtCore.Qt.AlignRight)

        compassBox = QtGui.QGroupBox('Magnetometer')
        compassBox.layout = QtGui.QGridLayout()
        compassBox.layout.addWidget(QtGui.QLabel('x:'), 0, 0)
        compassBox.layout.addWidget(QtGui.QLabel('y:'), 1, 0)
        compassBox.layout.addWidget(QtGui.QLabel('z:'), 2, 0)
        compassBox.layout.addWidget(self.compassX, 0, 1)
        compassBox.layout.addWidget(self.compassY, 1, 1)
        compassBox.layout.addWidget(self.compassZ, 2, 1)
        compassBox.layout.addWidget(QtGui.QLabel('Gauss'), 0, 2)
        compassBox.layout.addWidget(QtGui.QLabel('Gauss'), 1, 2)
        compassBox.layout.addWidget(QtGui.QLabel('Gauss'), 2, 2)
        compassBox.setLayout(compassBox.layout)

        self.barroPressure = QtGui.QLabel()
        self.barroHeight = QtGui.QLabel()

        barroBox = QtGui.QGroupBox('Magnetometer')
        barroBox.layout = QtGui.QGridLayout()
        barroBox.layout.addWidget(QtGui.QLabel('p:'), 0, 0)
        barroBox.layout.addWidget(QtGui.QLabel('h:'), 1, 0)
        barroBox.layout.addWidget(self.barroPressure, 0, 1)
        barroBox.layout.addWidget(self.barroHeight, 1, 1)
        barroBox.layout.addWidget(QtGui.QLabel('Pa'), 0, 2)
        barroBox.layout.addWidget(QtGui.QLabel('m'), 1, 2)
        barroBox.setLayout(barroBox.layout)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(gyroBox)
        self.layout.addWidget(accelBox)
        self.layout.addWidget(compassBox)
        self.layout.addWidget(barroBox)
        self.setLayout(self.layout)


    def gyroData(self, x, y, z):
        self.gyroX.setText(str(x))
        self.gyroY.setText(str(y))
        self.gyroZ.setText(str(z))


    def accelData(self, x, y, z):
        self.accelX.setText(str(x))
        self.accelY.setText(str(y))
        self.accelZ.setText(str(z))


    def compassData(self, x, y, z):
        self.compassX.setText(str(x))
        self.compassY.setText(str(y))
        self.compassZ.setText(str(z))


    def barroData(self, pressure, height):
        self.barroPressure.setText(str(pressure))
        self.barroHeight.setText(str(height))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    sensors = RawSensorWidget(None)
    sensors.show()
    sys.exit(app.exec_())
