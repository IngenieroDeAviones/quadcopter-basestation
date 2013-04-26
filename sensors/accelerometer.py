
from sensors import sensor

class Accelerometer(sensor.Sensor3D):
    char = 'A'
    def __init__(self, bufferLength=200, name = None):
        super().__init__(units = 'g', bufferLength = bufferLength, name = name)

