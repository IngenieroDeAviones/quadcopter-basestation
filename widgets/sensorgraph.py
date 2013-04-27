
from PyQt4 import QtCore, QtGui

import plotwidget

import os
import sys
sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))] + sys.path
import recorder


class SensorTreeWidget(QtGui.QTreeWidget):
    def __init__(self, sensors, parent=None):
        super().__init__(parent)
        self.setColumnCount(1)
        self.header().close()
        self.setSelectionMode(self.ExtendedSelection)

        for sensor in sensors:
            item = QtGui.QTreeWidgetItem(self, [sensor.name])
            item.sensor = sensor
            for name, channel in sensor.channels.items():
                widget = QtGui.QTreeWidgetItem(item, [name])
                widget.channel = channel
            item.setExpanded(True)
            self.addTopLevelItem(item)



class SensorGraph(plotwidget.PlotWidget):
    def __init__(self, parser, sensors, parent=None):
        super().__init__(parent)
        self.parser = parser
        self.sensors = sensors
        self.graphs = {}
        for i, sensor in enumerate(self.sensors):
            sensor.dataAdded.connect(self.replot)
            for channel in sensor.channels.values():
                data = channel.data
                graph = self.newGraph(data[0], data[1])
                graph.setVisible(False)
                self.graphs[channel] = graph
#        self.parser.nextIteration.connect(self.replot)


class SensorGraphWidget(QtGui.QWidget):
    def __init__(self, parser, sensors, parent=None):
        super().__init__(parent)

        self.parser = parser
        self.sensorTree = SensorTreeWidget(sensors)
        self.sensorTree.setMaximumWidth(200)
        self.sensorTree.selectionModel().selectionChanged.connect(self.selectionChanged)
        self.recordButton = QtGui.QPushButton('record')
        self.recordButton.clicked.connect(self.record)
        self.graph = SensorGraph(parser, sensors)

        leftLayout = QtGui.QVBoxLayout()
        leftLayout.addWidget(self.sensorTree)
        leftLayout.addWidget(self.recordButton)

        layout = QtGui.QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addWidget(self.graph)
        self.setLayout(layout)


    def selectionChanged(self, new, old):
        graphs = []
        for widget in self.sensorTree.selectedItems():
            try:
                graphs.append(self.graph.graphs[widget.channel])
            except:
                pass

        for graph in self.graph.graphs.values():
            graph.setVisible(graph in graphs)


    def record(self):
        channels = []
        for widget in self.sensorTree.selectedItems():
            try:
                channels.append(widget.channel)
            except:
                pass
        self.dialog = recorder.RecordDialog(self.parser, channels)
        self.dialog.show()



if __name__ == '__main__':
    import parser
    from sensors import gyroscope, accelerometer, magnetometer, barrometer

    sensorList = [gyroscope.Gyroscope(),
                  accelerometer.Accelerometer(),
                  magnetometer.Magnetometer(),
                  barrometer.Barrometer()]

    app = QtGui.QApplication(sys.argv)
    thread = parser.ParserThread('/dev/arduino')
    thread.daemon = True
    thread.start()
    sensorParser = parser.SensorDataParser(thread, sensorList)
    widget = SensorGraphWidget(thread, sensorParser.sensors.values())
    widget.show()
    sys.exit(app.exec_())
