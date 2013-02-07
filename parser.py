#! /usr/bin/env python3

from PyQt4 import QtCore


class InvalidSyntaxError(Exception):
    pass



class ParserThread(QtCore.QThread):
    notification = QtCore.pyqtSignal(list, str)
    error = QtCore.pyqtSignal(list, str)
    sensorData = QtCore.pyqtSignal(list, list)


    def __init__(self, stream):
        super().__init__()
        self.stream = stream


    def parseLine(self, line):
        try:
            command, *arguments = line.strip().split(' ')
        except:
            raise InvalidSyntaxError()

        cmd, *cmd_type = command

        if cmd == 'N':
            self.notification.emit(cmd_type, ' '.join(arguments))
        elif cmd == 'E':
            self.error.emit(cmd_type, ' '.join(arguments))
        elif cmd == 'S':
            self.sensorData.emit(cmd_type, arguments)


    
    def run(self):
        for line in self.stream:
            try:
                self.parseLine(line)
            except Exception as e:
                print(e)


class SensorDataParser(QtCore.QObject):
    gyroscopeData = QtCore.pyqtSignal(float, float, float)
    accelerometerData = QtCore.pyqtSignal(float, float, float)
    magnetometerData = QtCore.pyqtSignal(float, float, float)
    barrometerData = QtCore.pyqtSignal(float)
    gpsData = QtCore.pyqtSignal(float, float, float, float)
    currentData = QtCore.pyqtSignal(str, list)
    temperatureData = QtCore.pyqtSignal(str, list)

    def __init__(self, parserThread):
        super().__init__()
        parserThread.sensorData.connect(self.parseData)


    def parseData(self, sensor, data):
        if sensor[0] == 'G':
            self.gyroscopeData.emit(*map(float, data[:3]))
        elif sensor[0] == 'A':
            self.accelerometerData.emit(*map(float, data[:3]))
        elif sensor[0] == 'M':
            self.magnetometerData.emit(*map(float, data[:3]))
        elif sensor[0] == 'B':
            self.barrometerData.emit(float(data[0]))
        elif sensor[0] == 'P':
            pass
        elif sensor[0] == 'C':
            pass
        elif sensor[0] == 'T':
            pass

