
from collections import deque, OrderedDict
import datetime
import configparser

from PyQt4 import QtCore


class Channel:
    def __init__(self, sensor, name, unit=None, bufferLength=200):
        self.sensor = sensor
        self.name = name
        self.data = [deque(maxlen=bufferLength), deque(maxlen=bufferLength)]
        self.units = unit


    def data(self):
        return sensor.channel[self.name]


    def __len__(self):
        return len(self.data[0])


    def __iadd__(self, t):
        self.data[0].append(t[0])
        self.data[1].append(t[1])
        return self



class Sensor(QtCore.QObject):
    dataAdded = QtCore.pyqtSignal(datetime.datetime, list)
    calibration = {}

    def __init__(self, channelNames, units=None, bufferLength=200, name=None):
        super().__init__()
        self.name = name or self.__class__.__name__
        if type(units) == str or units is None:
            units = [units] * len(channelNames)

        self.channels = OrderedDict([ (channelName, Channel(self, channelName, unit, bufferLength)) for channelName, unit in zip(channelNames, units)])
        self.loadCalibration()


    def appendData(self, data, timestamp=None):
        data = list(map(float, data))
        if timestamp is None:
            timestamp = datetime.datetime.now()
        for channel, d in zip(self.channels.values(), data):
            channel += [timestamp, d]
        self.dataAdded.emit(timestamp, data)
        return timestamp


    def calibrate(self):
        pass


    def loadCalibration(self, calibrationFile='data/calibration.ini'):
        f = configparser.RawConfigParser()
        f.read(calibrationFile)
        print(self.name)
        try:
            self.calibration = { key: float(value) for (key, value) in f[self.name].items()}
            print(self.calibration)
        except Exception as e:
            print(e)
            pass


    def saveCalibration(self, calibrationFile='data/calibration.ini'):
        f = configparser.RawConfigParser()
        f.read(calibrationFile)
        f[self.name] = self.calibration
        f.write(open(calibrationFile,'w'))


    def __getitem__(self, key):
        return self.channels[key]


    def __iter__(self):
        return iter(self.channels.values())


class Sensor3D(Sensor):
    def __init__(self, channelNames =['x', 'y', 'z'], units=None, bufferLength=200, name=None):
        super().__init__(channelNames = channelNames, units = units, bufferLength = bufferLength, name = name)

