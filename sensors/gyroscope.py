
from sensors import sensor

class Gyroscope(sensor.Sensor3D):
    char = 'G'
    def __init__(self, bufferLength=200, name = None):
        super().__init__(units = '°/s', bufferLength = bufferLength, name = name)

