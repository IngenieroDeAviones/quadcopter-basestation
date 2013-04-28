#! /usr/bin/env python3

import os
import sys

import numpy as np

from PyQt4 import QtCore, QtGui

sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))] + sys.path
import parser
import magnetometer
import accelerometer


n = 200

def fitEllipsoid(x, y, z):
    x = x[:,np.newaxis]
    y = y[:,np.newaxis]
    z = z[:,np.newaxis]
    D = np.hstack((x*x, y*y, z*z, x, y, z, np.ones_like(x)))
    S = np.dot(D.T, D)
    C = np.zeros([7,7])
    C[0,1] = C[1,0] = 2;
    E, V = np.linalg.eig(np.dot(np.linalg.inv(S), C))
    n = np.argmax(np.abs(E))
    a = V[:,n]
    return a

def ellipsoid_center(a):
    A,B,C,D,E,F,G = a
    x0=-D/(2*A)
    y0=-E/(2*B)
    z0=-F/(2*C)
    return [x0,y0,z0]

def ellipsoid_axis_length( a ):
    A,B,C,D,E,F,G = a
    res1=np.sqrt( (B*C*D*D + A*C*E*E + A*B*F*F - A*B*C*G) / (np.sqrt(2) * A*A*B*C) )
    res2=np.sqrt( (B*C*D*D + A*C*E*E + A*B*F*F - A*B*C*G) / (np.sqrt(2) * A*B*B*C) )
    res3=np.sqrt( (B*C*D*D + A*C*E*E + A*B*F*F - A*B*C*G) / (np.sqrt(2) * A*B*C*C) )
    return [res1, res2, res3]

def calibrate(sensor):
    print(sensor)
    x = np.array(sensor['rawx'].data[1])
    y = np.array(sensor['rawy'].data[1])
    z = np.array(sensor['rawz'].data[1])

    a = fitEllipsoid(x,y,z)
    center = ellipsoid_center(a)
    axes = ellipsoid_axis_length(a)

    print("center = ",  center)
    print("axes = ", axes)

    sensor.calibration['cx'] = center[0]
    sensor.calibration['cy'] = center[1]
    sensor.calibration['cz'] = center[2]

    sensor.calibration['a'] = axes[0]
    sensor.calibration['b'] = axes[1]
    sensor.calibration['c'] = axes[2]

    sensor.saveCalibration()


def newData(t, d):
    if len(compass['rawx']) >= n and len(accelerometer['rawx']) >= n:
        compass.dataAdded.disconnect()
        accelerometer.dataAdded.disconnect()
        print('Done collecting data, finding best fit ellipsoid.')
        calibrate(compass)
        calibrate(accelerometer)

        sys.exit()


app = QtGui.QApplication(sys.argv)

compass = magnetometer.Magnetometer(bufferLength=n)
compass.dataAdded.connect(newData)
accelerometer = accelerometer.Accelerometer(bufferLength=n)
accelerometer.dataAdded.connect(newData)

thread = parser.ParserThread('/dev/arduino')
thread.daemon = False
thread.start()
sensorParser = parser.SensorDataParser(thread, [compass, accelerometer])

sys.exit(app.exec_())
