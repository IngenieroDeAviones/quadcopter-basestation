
from PyQt4 import QtCore, QtGui

import plotwidget


class SensorTreeWidget(QtGui.QTreeWidget):
    def __init__(self, sensors, parent=None):
        super().__init__(parent)
        self.setColumnCount(1)
        self.header().close()
        self.setSelectionMode(self.ExtendedSelection)

        for sensor in sensors:
            item = QtGui.QTreeWidgetItem(self, [sensor.name])
            for channel in sensor.channels:
                QtGui.QTreeWidgetItem(item, [channel])
            item.setExpanded(True)
            self.addTopLevelItem(item)


class SensorGraph(plotwidget.PlotWidget):
    def __init__(self, sensors, parent=None):
        super().__init__(parent)
        self.sensors = sensors
        self.graphs = []
        for i, sensor in enumerate(self.sensors):
            sensor.dataAdded.connect(self.replot)
            for channel in sensor.channels:
                data = sensor.data[channel]
                self.graphs.append(self.newGraph(data[0], data[1]))


class SensorGraphWidget(QtGui.QWidget):
    def __init__(self, sensors, parent=None):
        super().__init__(parent)

        self.sensorTree = SensorTreeWidget(sensors)
        self.sensorTree.setMaximumWidth(200)
#        self.sensorTree.selectionChanged.connect(self.selectionChanged)
        self.graph = SensorGraph(sensors)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.sensorTree)
        layout.addWidget(self.graph)
        self.setLayout(layout)

    def selectionChanged(new, old):
        print(new)



if __name__ == '__main__':
    import os
    import sys
    sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))] + sys.path
    import parser
    import sensor

    sensorList = [sensor.Gyroscope(),
                  sensor.Accelerometer(),
                  sensor.Magnetometer(),
                  sensor.Barrometer()]

    app = QtGui.QApplication(sys.argv)
    thread = parser.ParserThread('/dev/arduino')
    thread.start()
    sensorParser = parser.SensorDataParser(thread, sensorList)
    widget = SensorGraphWidget(sensorParser.sensors.values())
    widget.show()
    sys.exit(app.exec_())
