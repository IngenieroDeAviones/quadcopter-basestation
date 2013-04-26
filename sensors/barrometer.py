
from sensors import sensor

class Barrometer(sensor.Sensor):
    char = 'B'
    def __init__(self, bufferLength=200, name = None):
        super().__init__(channelNames = ['pressure', 'height'], units = ['Pa', 'm'], bufferLength = bufferLength, name = name)
