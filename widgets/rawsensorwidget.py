
from PyQt4 import QtCore, QtGui


class RawSensorWidget(QtGui.QWidget):
    def __init__(self, sensors):
        super().__init__()

        layout = QtGui.QVBoxLayout()

        self.labels = {}
        for sensor in sensors:
            widget = QtGui.QGroupBox(sensor.name)
            sublayout = QtGui.QGridLayout()
            channelLabels = {}
            for row, channel in enumerate(sensor.channels):
                channelLabel = QtGui.QLabel()
                channelLabel.setAlignment(QtCore.Qt.AlignRight)
                channelLabels[channel] = channelLabel
                sublayout.addWidget(QtGui.QLabel(channel + ':'), row, 0)
                sublayout.addWidget(channelLabel, row, 1)
                sublayout.addWidget(QtGui.QLabel(sensor.units[channel]), row, 2)
            widget.setLayout(sublayout)
            layout.addWidget(widget)
            self.labels[sensor.name] = channelLabels
            
            sensor.dataAdded.connect(self.updateSensor)
                
        self.setLayout(layout)

    def updateSensor(self, data):
        sensor = self.sender()
        labels = self.labels[sensor.name]
        for channel in sensor.channels:
            labels[channel].setText(str(sensor.data[channel][1][-1]))



if __name__ == '__main__':
    import os
    import sys
    sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))] + sys.path
    import parser
    from sensors import sensor
    from processing import estimator

    sensorList = [sensor.Gyroscope(),
                  sensor.Accelerometer(),
                  sensor.Magnetometer(),
                  sensor.Barometer()]

    app = QtGui.QApplication(sys.argv)
    estimator = estimator.Estimator(sensor.SensorManager())
    widget = RawSensorWidget(estimator.sensors.values())
    widget.show()
    sys.exit(app.exec_())
