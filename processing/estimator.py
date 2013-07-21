
import math

from PyQt4 import QtCore

from sensors import sensor
import parser
import stream
from processing import filters


class Estimator:

    def __init__(self, sensors):
        super().__init__()
        self.rotation_raw = stream.Stream(('pitch', 'roll', 'heading'), name='estimator.rotation_raw')

        self.sensors = sensors
        self.sensors.accelerometer.updated.connect(self.updateRotation)
        self.sensors.magnetometer.updated.connect(self.updateRotation)

        self.rotation = filters.Complementary(self.rotation_raw, self.sensors.gyroscope, tau=2, name='estimator.rotation')


    def updateRotation(self, stream):
        mx, my, mz = [self.sensors.magnetometer[c] for c in ('x','y','z')]
        ax, ay, az = [self.sensors.accelerometer[c] for c in ('x','y','z')]

        roll = math.atan2(-ay,az)
        pitch = math.atan2(ax, math.sqrt(ay*ay + az*az))
        heading = math.atan2(mx * math.sin(pitch) * math.sin(roll) + my * math.cos(roll) + mz * math.cos(pitch) * math.sin(roll),
                                  mx * math.cos(pitch) - mz * math.sin(pitch))

        self.rotation_raw.update((pitch, roll, heading))
