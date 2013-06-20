
import math

from PyQt4 import QtCore

from sensors import sensor
import parser
import stream
from processing import filters


class Estimator:

    def __init__(self):
        super().__init__()
        self.rotation_raw = stream.Stream(('pitch', 'roll', 'heading'), name='estimator.rotation_raw')

        self.thread = parser.ParserThread('/dev/arduino')
        self.sensorParser = parser.SensorDataParser(self.thread)
        self.thread.start()

        self.accelerometer = sensor.Accelerometer(self.sensorParser)
        self.accelerometer.updated.connect(self.updateRotation)
        self.magnetometer = sensor.Magnetometer(self.sensorParser)
        self.magnetometer.updated.connect(self.updateRotation)
        self.gyroscope = sensor.Gyroscope(self.sensorParser)

        self.rotation = filters.Complementary(self.rotation_raw, self.gyroscope, tau=2, name='estimator.rotation')


    def updateRotation(self, stream):
        mx, my, mz = [self.magnetometer[c] for c in ('x','y','z')]
        ax, ay, az = [self.accelerometer[c] for c in ('x','y','z')]

        roll = math.atan2(-ay,az)
        pitch = math.atan2(ax, math.sqrt(ay*ay + az*az))
        heading = math.atan2(mx * math.sin(pitch) * math.sin(roll) + my * math.cos(roll) + mz * math.cos(pitch) * math.sin(roll),
                                  mx * math.cos(pitch) - mz * math.sin(pitch))

        self.rotation_raw.update((pitch, roll, heading))
