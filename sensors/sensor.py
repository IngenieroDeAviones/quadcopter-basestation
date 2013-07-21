
import datetime
import configparser

from PyQt4 import QtCore

import stream
import parser


class Sensor(stream.Stream):
    calibration = {}

    def __init__(self, channelNames, name=None):
        name = str(name) if not name is None else self.__class__.__name__
        stream.Stream.__init__(self, channelNames, name = 'sensor.' + name)
        self.raw = stream.Stream(channelNames, self.name + '_raw')
        self.loadCalibration()

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
            name = self.name.split('.', maxsplit=-1)[1]
            self.calibration = { key: float(value) for (key, value) in f[name].items() }
        except:
            pass


    def saveCalibration(self, calibrationFile='data/calibration.ini'):
        f = configparser.RawConfigParser()
        f.read(calibrationFile)
        f[self.name] = self.calibration
        f.write(open(calibrationFile,'w'))


class Sensor3D(Sensor):
    calibration = {'cx': 0, 'cy': 0, 'cz': 0, 'a': 1, 'b': 1, 'c': 1}
    def __init__(self, name=None, channelNames=None):
        super().__init__(channelNames = channelNames or ['x', 'y', 'z'], name = name)


    def newData(self, stream):
        x = (float(stream['x']) - self.calibration['cx']) / self.calibration['a']
        y = (float(stream['y']) - self.calibration['cy']) / self.calibration['b']
        z = (float(stream['z']) - self.calibration['cz']) / self.calibration['c']
        self.update([x,y,z])


#######################################
# Individual sensors:

class Accelerometer(Sensor3D):
    pass


class Magnetometer(Sensor3D):
    pass


class Gyroscope(Sensor3D):
    pass


class Barometer(Sensor):
    def __init__(self, channelNames="pressure", name=None):
        super().__init__(channelNames, name)


#######################################
# Sensor manager class

class SensorManager:
    def __init__(self):
        self.thread = parser.ParserThread('/dev/arduino', self)

        self.accelerometer = Accelerometer()
        self.magnetometer = Magnetometer()
        self.gyroscope = Gyroscope()
        self.barometer = Barometer()

        self.thread.start()

