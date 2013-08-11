#! /usr/bin/env python3

import struct
import serial

from PyQt4 import QtCore


welcomeMessage = b"- Arduino Start -\n"


class InvalidSyntaxError(Exception):
    pass



class ParserThread(QtCore.QThread):
    daemon = True

    commandRecieved = QtCore.pyqtSignal(bytes)
    error = QtCore.pyqtSignal(bytes)

    def __init__(self, device, sensors):
        super().__init__()
        if type(device) == str:
            try:
                device = serial.Serial(device, 115200)
            except:
                print('Warning: not connected to arduino')
                device = None
        self.stream = device
        self.sensors = sensors


    def parseCommand(self):
        c = ord(self.stream.read(1))

        length = (c >> 4) & 0b1111
        cmd = c & 0b1111

        data = self.stream.read(length)

        self.commandRecieved.emit(struct.pack('B', c) + data);

        if cmd == 0x1:
            self.error.emit(data)
        elif cmd == 0x2:
            self.sensors.barometer.update(struct.unpack('f', data))
        elif cmd == 0x3:
            self.sensors.gyroscope.update(struct.unpack('fff', data))
        elif cmd == 0x4:
            self.sensors.accelerometer.update(struct.unpack('fff', data))
        elif cmd == 0x5:
            self.sensors.magnetometer.update(struct.unpack('fff', data))


    def send(self, command):
        print(command)
        self.stream.write(command)

    
    def run(self):
        if self.stream:
            self.stream.flush()
            self.send(b'\x01')
            while True:
                self.parseCommand()


    def __del__(self):
        if self.stream:
            self.stream.close()
