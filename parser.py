#! /usr/bin/env python3

from PyQt4 import QtCore


class InvalidSyntaxError(Exception):
    pass



class ParserThread(QtCore.QThread):
    notification = QtCore.pyqtSignal(str, str)
    error = QtCore.pyqtSignal(str, str)
    sensorData = QtCore.pyqtSignal(list)


    def __init__(self, stram):
        super().__init()
        self.stream = stream


    def parseLine(self, line):
        try:
            command, *arguments = line.split(' ')
        except:
            raise InvalidSyntaxError()

        cmd, *cmd_type = command

        if cmd == 'N':
            self.notification.send(cmd_type, ' '.join(arguments))
        elif cmd == 'E':
            self.error.send(cmd_type, ' '.join(arguments))
        elif cmd == 'S':
            self.sensorData.send(cmd_type, arguments)


    
    def run(self):
        data = ''
        try:
            data += self.stream.readall()
            lines = data.split('\n')
            for line in lines:
                self.parseLine(line)
            data = lines[-1]
        except:
            print(e)
            pass


class SensorDataParser:
    gyroscopeData = QtCore.pyqtSignal(float, float, float)
    accelerometerData = QtCore.pyqtSignal(float, float, float)
    magnetometerData = QtCore.pyqtSignal(float, float, float)
    barrometerData = QtCore.pyqtSignal(float)

    def __init__(self, parserThread):
        
