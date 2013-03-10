
from collections import deque, OrderedDict
import datetime

from PyQt4 import QtCore


class Channel:
    def __init__(self, sensor, name, unit=None, bufferLength=200):
        self.sensor = sensor
        self.name = name
        self.data = [deque(maxlen=bufferLength), deque(maxlen=bufferLength)]
        self.units = unit


    def data(self):
        return sensor.channel[self.name]



class Sensor(QtCore.QObject):
    dataAdded = QtCore.pyqtSignal(list)

    def __init__(self, channelNames, units=None, bufferLength=200, name=None):
        super().__init__()
        self.name = name or self.__qualname__
        if type(units) == str or units is None:
            units = [units] * len(channelNames)

        self.channels = OrderedDict([ (channelName, Channel(self, channelName, unit, bufferLength)) for channelName, unit in zip(channelNames, units)])


    def appendData(self, data, timestamp=None):
        data = list(map(float, data))
        if timestamp is None:
            timestamp = datetime.datetime.now()
        for channel, d in zip(self.channels.values(), data):
            channel.data[0].append(timestamp)
            channel.data[1].append(d)
        self.dataAdded.emit(data)


class Sensor3D(Sensor):
    def __init__(self, channelNames =['x', 'y', 'z'], units=None, bufferLength=200, name=None):
        super().__init__(channelNames = channelNames, units = units, bufferLength = bufferLength, name = name)


class Gyroscope(Sensor3D):
    char = 'G'
    def __init__(self, bufferLength=200, name = None):
        super().__init__(units = '°/s', bufferLength = bufferLength, name = name)


class Magnetometer(Sensor3D):
    char = 'M'
    def __init__(self, bufferLength=200, name = None):
        super().__init__(channelNames = ['x', 'y', 'z', 'heading'], units = ['Gauss']*3 + ['degrees'], bufferLength = bufferLength, name = name)


class Accelerometer(Sensor3D):
    char = 'A'
    def __init__(self, bufferLength=200, name = None):
        super().__init__(units = 'g', bufferLength = bufferLength, name = name)


class Barrometer(Sensor):
    char = 'B'
    def __init__(self, bufferLength=200, name = None):
        super().__init__(channelNames = ['pressure', 'height'], units = ['Pa', 'm'], bufferLength = bufferLength, name = name)
