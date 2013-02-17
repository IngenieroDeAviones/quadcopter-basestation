#! /usr/bin/env python3

from PyQt4 import QtCore


class InvalidSyntaxError(Exception):
    pass



class ParserThread(QtCore.QThread):
    daemon = True

    notification = QtCore.pyqtSignal(list, str)
    error = QtCore.pyqtSignal(list, str)
    sensorData = QtCore.pyqtSignal(list, list)

    def __init__(self, stream):
        super().__init__()
        if type(stream) == str:
            stream = open(stream)
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
    def __init__(self, parserThread, **sensors):
        super().__init__()
        parserThread.sensorData.connect(self.parseData)
        self.sensors = sensors


    def parseData(self, sensor, data):
        if sensor[0] in self.sensors:
            self.sensors[sensor[0]].appendData(data)
