
from collections import deque
import datetime

class Sensor(dict):
    dataAdded = QtCore.pyqtSignal(list)

    def __init__(self, channels, units=None, bufferLength=1e3):
        self.data = {}
        self.channels = channels
        elif type(units) == str or units is None:
            units = [units] * len(channels)
        for channel, unit in channels:
            self[channel] = deque(maxlen=bufferLength)
            self[channel].unit = unit


    def appendData(self, timestamp=None, *data):
        if timestamp is None:
            timestamp = datetime.datetime.now()
        for channel, d in zip(self.channels, data):
            self[channel].append([timestamp, d])


class Sensor3D(Sensr):
    def __init__(self, units=None, bufferLength=1e3):
        super().__init__(channels = ['x', 'y', 'z'], units = units, bufferLength = bufferLength)


class Gyroscope(Sensor3D):
    def __init__(self, bufferLength=1e3):
        super().__init__(units = '°/s', bufferLength = bufferLength)


class Magnetometer(Sensor3D):
    def __init__(self, bufferLength=1e3):
        super().__init__(units = 'Gauss', bufferLength = bufferLength)


class Accelerometer(Sensor3D):
    def __init__(self, bufferLength=1e3):
        super().__init__(units = 'g', bufferLength = bufferLength)


class Barrometer(Sensor):
    def __init__(self, bufferLength=1e3):
        super().__init__(channels = ['pressure', 'height'], units = ['Pa', 'm'], bufferLength = bufferLength)
