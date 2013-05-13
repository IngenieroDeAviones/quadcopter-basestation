
import datetime
import configparser

from PyQt4 import QtCore

import stream


class Sensor(stream.Stream):
    calibration = {}

    def __init__(self, sensorDataParser, channelNames, name=None):
        super().__init__(channelNames)
        self.raw = stream.Stream(channelNames)
        self.name = name or self.__class__.__name__
        self.loadCalibration()

        sensorDataParser.addStream(self.char, self.raw)
        self.raw.updated.connect(self.newData)


    def newData(self, stream):
        """Called when new data is available.
        
        Overload this function to implement calibration. You do not have
        to use super in that case.

        """
        self.update(stream._channels)


    def calibrate(self):
        pass


    def loadCalibration(self, calibrationFile='data/calibration.ini'):
        f = configparser.RawConfigParser()
        f.read(calibrationFile)
        try:
            self.calibration = { key: float(value) for (key, value) in f[self.name].items() }
        except:
            pass


    def saveCalibration(self, calibrationFile='data/calibration.ini'):
        f = configparser.RawConfigParser()
        f.read(calibrationFile)
        f[self.name] = self.calibration
        f.write(open(calibrationFile,'w'))


class Sensor3D(Sensor):
    calibration = {'cx': 0, 'cy': 0, 'cz': 0, 'a': 1, 'b': 1, 'c': 1}
    def __init__(self, sensorDataParser, name = None):
        super().__init__(sensorDataParser, channelNames = ['x', 'y', 'z'], name = name)


    def newData(self, stream):
        x = (float(stream['x']) - self.calibration['cx']) / self.calibration['a']
        y = (float(stream['y']) - self.calibration['cy']) / self.calibration['b']
        z = (float(stream['z']) - self.calibration['cz']) / self.calibration['c']
        self.update([x,y,z])


#######################################
# Individual sensors:

class Accelerometer(Sensor3D):
    char = 'A'


class Magnetometer(Sensor3D):
    char = 'M'


class Gyroscope(Sensor3D):
    char = 'G'


class Barometer(Sensor):
    char = 'B'
