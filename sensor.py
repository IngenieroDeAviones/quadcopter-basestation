
from collections import deque
import datetime

from PyQt4 import QtCore

class Sensor(QtCore.QObject):
    dataAdded = QtCore.pyqtSignal(list)

    def __init__(self, channels, units=None, bufferLength=1000, name=None):
        super().__init__()
        self.data = {}
        self.channels = channels
        self.units = {}
        self.name = name or self.__qualname__
        if type(units) == str or units is None:
            units = [units] * len(channels)
        for channel, unit in zip(channels, units):
            self.data[channel] = [deque(maxlen=bufferLength), deque(maxlen=bufferLength)]
            self.units[channel] = unit


    def appendData(self, data, timestamp=None):
        data = list(map(float, data))
        if timestamp is None:
            timestamp = datetime.datetime.now()
        for channel, d in zip(self.channels, data):
            self.data[channel][0].append(timestamp)
            self.data[channel][1].append(d)
        self.dataAdded.emit(data)


class Sensor3D(Sensor):
    def __init__(self, channels =['x', 'y', 'z'], units=None, bufferLength=1000, name=None):
        super().__init__(channels = channels, units = units, bufferLength = bufferLength)


class Gyroscope(Sensor3D):
    char = 'G'
    def __init__(self, bufferLength=1000, name = None):
        super().__init__(units = '°/s', bufferLength = bufferLength)


class Magnetometer(Sensor3D):
    char = 'M'
    def __init__(self, bufferLength=1000, name = None):
        super().__init__(channels = ['x', 'y', 'z', 'heading'], units = ['Gauss']*3 + ['degrees'], bufferLength = bufferLength)


class Accelerometer(Sensor3D):
    char = 'A'
    def __init__(self, bufferLength=1000, name = None):
        super().__init__(units = 'g', bufferLength = bufferLength)


class Barrometer(Sensor):
    char = 'B'
    def __init__(self, bufferLength=1000, name = None):
        super().__init__(channels = ['pressure', 'height'], units = ['Pa', 'm'], bufferLength = bufferLength)
