
import datetime
import collections

from PyQt4 import QtCore, QtGui

class Recorder(QtCore.QObject):
    finshed = QtCore.pyqtSignal()

    def __init__(self, parser, parent=None):
        super().__init__(parent)
        self.parser = parser
        pass


    def record(self, channels, filename, length):
        self.channels = channels
        self.f = open(filename, 'w')
        self.length = length
        self.i = 0
        self.data = collections.OrderedDict([(channel, None) for channel in self.channels])
        self.startTime = datetime.datetime.now()
        for sensor in set(channel.sensor for channel in self.channels):
            sensor.dataAdded.connect(self.newData)
        self.parser.nextIteration.connect(self.newIteration)
        self.f.write(self.line(['time'] + ['.'.join([channel.sensor.name, channel.name]) for channel in self.channels]))


    def newData(self, data):
        sensor = self.sender()
        for i, channel in enumerate(sensor.channels.values()):
            if channel in self.channels:
                self.data[channel] = data[i]


    def newIteration(self, i):
        dt = datetime.datetime.now() - self.startTime
        self.f.write(self.line(dt.total_seconds(), *self.data.values()))
        self.i += 1
        if self.i == self.length:
            for sensor in set(channel.sensor for channel in self.channels):
                sensor.dataAdded.disconnect(self.newData)
            self.parser.nextIteration.disconnect()
            self.finshed.emit()
            self.f.close()


    def line(self, *data):
        return ','.join(map(str, data)) + '\n'
        


class RecordDialog(QtGui.QDialog):
    def __init__(self, parser, channels, parent=None):
        super().__init__(parent)

        self.parser = parser
        self.channels = channels

        self.setFixedWidth(500)

        layout = QtGui.QGridLayout()
        layout.addWidget(QtGui.QLabel('Filename: '), 0 ,0)
        self.fileNameEdit = QtGui.QLineEdit('measurement.csv')
        layout.addWidget(self.fileNameEdit, 0, 1)
        layout.addWidget(QtGui.QLabel('Datapoints: '), 1, 0)
        self.lengthSpinBox = QtGui.QSpinBox()
        self.lengthSpinBox.setMinimum(1)
        self.lengthSpinBox.setMaximum(1e6)
        self.lengthSpinBox.setValue(100)
        layout.addWidget(self.lengthSpinBox, 1, 1)
        self.recordButton = QtGui.QPushButton('Record')
        self.recordButton.clicked.connect(self.startRecord)
        layout.addWidget(self.recordButton, 2, 0)
        self.setLayout(layout)

    def startRecord(self):
        self.recorder = Recorder(self.parser, self)
        self.recorder.record(self.channels, self.fileNameEdit.text(), self.lengthSpinBox.value())
        self.setEnabled(False)
        self.recorder.finshed.connect(self.recordingFinished)


    def recordingFinished(self):
        self.close()
