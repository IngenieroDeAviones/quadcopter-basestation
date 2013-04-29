
import math

from PyQt4 import QtCore

from sensors import accelerometer, magnetometer
import parser

class Estimator(QtCore.QObject):
    newRotation = QtCore.pyqtSignal(float, float, float)
    roll = 0
    pitch = 0
    heading = 0

    def __init__(self):
        super().__init__()
        self.accelerometer = accelerometer.Accelerometer()
        self.accelerometer.dataAdded.connect(self.updateRotation)
        self.magnetometer = magnetometer.Magnetometer()
        self.magnetometer.dataAdded.connect(self.updateRotation)
        self.thread = parser.ParserThread(open('/dev/arduino'))
        self.sensorParser = parser.SensorDataParser(self.thread, [self.accelerometer, self.magnetometer])
        self.thread.start()


    def updateRotation(self, timestamp, data):
        mx, my, mz = [self.magnetometer[c].latest() for c in ('x','y','z')]
        ax, ay, az = [self.accelerometer[c].latest() for c in ('x','y','z')]

        self.roll = math.atan2(-ay,az)
        self.pitch = math.atan2(ax, math.sqrt(ay*ay + az*az))
        self.heading = math.atan2(my, mx)

        self.newRotation.emit(self.roll, self.pitch, self.heading)
