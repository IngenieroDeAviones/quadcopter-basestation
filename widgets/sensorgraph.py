
from PyQt4 import QtCore, QtGui

import graphwidget


class SensorTreeWidget(QtGui.QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(1)
        self.header().close()
        self.setSelectionMode(self.ExtendedSelection)

        item = QtGui.QTreeWidgetItem(self, ['Gyroscope'])
        QtGui.QTreeWidgetItem(item, ['x'])
        QtGui.QTreeWidgetItem(item, ['y'])
        QtGui.QTreeWidgetItem(item, ['z'])
        item.setExpanded(True)
        self.addTopLevelItem(item)

        item = QtGui.QTreeWidgetItem(self, ['Accelerometer'])
        QtGui.QTreeWidgetItem(item, ['x'])
        QtGui.QTreeWidgetItem(item, ['y'])
        QtGui.QTreeWidgetItem(item, ['z'])
        item.setExpanded(True)
        self.addTopLevelItem(item)

        item = QtGui.QTreeWidgetItem(self, ['Magnetometer'])
        QtGui.QTreeWidgetItem(item, ['x'])
        QtGui.QTreeWidgetItem(item, ['y'])
        QtGui.QTreeWidgetItem(item, ['z'])
        item.setExpanded(True)
        self.addTopLevelItem(item)

        item = QtGui.QTreeWidgetItem(self, ['Barrometer'])
        QtGui.QTreeWidgetItem(item, ['pressure'])
        QtGui.QTreeWidgetItem(item, ['height'])
        item.setExpanded(True)
        self.addTopLevelItem(item)


class SensorGraph(graphwidget.GraphWidget):
    def __init__(self, sensorParser, parent=None)
        super().__init__(parent)
        self.sensors = {
                'Gyroscope.x': None,
                'Gyroscope.y': None,
                'Gyroscope.z': None,
                'Accelerometer.x': None,
                'Accelerometer.y': None,
                'Accelerometer.z': None,
                'Magnetometer.x': None,
                'Magnetometer.y': None,
                'Magnetometer.z': None,
                'Barrometer.pressure': None,
                'Barrometer.height': None
            }
        for key in self.sensors:
            self.sensors[key] = self.addGraph([], [])

        self.sensorParser = sensorParser
        sensorParser.gyroscopeData.connect(gyroData)
#        sensorParser.gyroscopeData.connect(lambda *new: appendData('Gyroscope', new))
#        sensorParser.accelerometerData.connect(lambda *new: appendData('Accelerometer', new))
#        sensorParser.magnetometerData.connect(lambda *new: appendData('Magnetometer', new))
#        sensorParser.barrometerData.connect(lambda *new: appendData('barrometer', new))

        self.n = 1000


    def replot(self)
        for data in self.plotSet:
            axis.plot()

    def gyroData(self, x, y, z):
        self.data[self.sensors['Magnetometer.x']][0]._y.append(x)

    def appendData(self, dataset, newdata):
        if len(dataset) >= self.n):
            dataset = [self.sensors[dataset + p][1:] + [newdata[i] for i,p in enumerate(('x','y','z'))]
        else:
            for i in range(3):
                dataset[i].append(newdata[i])
        self.replot()


    def setPlotSet(self, plotSet):
        plotSet = {self.sensors[name] for name in plotSet}
        self.replot()
            



class SensorGraphWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.sensorTree = SensorTreeWidget(self)
#        self.sensorTree.selectionChanged.connect(self.selectionChanged)
        self.graph = graphwidget.GraphWidget(self)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.sensorTree)
        layout.addWidget(self.graph)
        self.setLayout(layout)

#    def selectionChanged(new, old):
#        self.graph.
        


if __name__ == '__main__':
    import os
    import sys
    sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))] + sys.path
    import parser

    app = QtGui.QApplication(sys.argv)
    widget = SensorGraphWidget(None)
    widget.show()
    sys.exit(app.exec_())
