#! /usr/bin/env python3

import os
import sys

from PyQt4 import QtCore, QtGui

sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))] + sys.path
import parser
import magnetometer


n = 20


def calibrate(data):
    pass


def newData(t, d):
    if len(compass['x']) >= n:
        compass.dataAdded.disconnect()
        print('Done collecting data, finding best fit ellipsoid.')
        calibrate()


app = QtGui.QApplication(sys.argv)

compass = magnetometer.Magnetometer(bufferLength=n)
compass.dataAdded.connect(newData)

thread = parser.ParserThread('/dev/arduino')
thread.daemon = False
thread.start()
sensorParser = parser.SensorDataParser(thread, [compass])

sys.exit(app.exec_())
