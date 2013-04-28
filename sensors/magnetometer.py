
from collections import OrderedDict

from sensors import sensor

class Magnetometer(sensor.Sensor3D):
    char = 'M'
    calibration = {'cx': 0, 'cy': 0, 'cz': 0, 'a': 1, 'b': 1, 'c': 1}
    def __init__(self, bufferLength=200, name = None):
        super().__init__(channelNames = ['rawx', 'rawy', 'rawz'], units = [None]*3, bufferLength = bufferLength, name = name)
        self.channels.update(OrderedDict([ (name, sensor.Channel(self, name, None, bufferLength)) for name in ['x', 'y', 'z']]))


    def appendData(self, data, timestamp=None):
        timestamp = super().appendData(data, timestamp)
        self.channels['x'] += [timestamp, (float(data[0]) - self.calibration['cx']) / self.calibration['a']]
        self.channels['y'] += [timestamp, (float(data[1]) - self.calibration['cy']) / self.calibration['b']]
        self.channels['z'] += [timestamp, (float(data[2]) - self.calibration['cz']) / self.calibration['c']]
