
from collections import deque
from PyQt4 import QtCore, QtGui

import plotwidget

import os
import sys
sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))] + sys.path
import recorder
from processing import estimator
import stream

class streamGraph(plotwidget.Graph):
    def __init__(self, axis, stream, channel):
        self.data = [deque(maxlen=200), deque(maxlen=200)]
        super().__init__(axis, self.data[0], self.data[1])
        self.channel = channel
        stream.updated.connect(self.update)
    

    def update(self, stream):
        self.data[0].append(stream.timestamp)
        self.data[1].append(stream[self.channel])


class SensorTreeWidget(QtGui.QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(1)
        self.header().close()
        self.setSelectionMode(self.ExtendedSelection)

        streams = stream.Stream.getInstances()
        for s in streams:
            item = QtGui.QTreeWidgetItem(self, [s.name])
            item.sensor = s
            for channel in s:
                widget = QtGui.QTreeWidgetItem(item, [channel])
                widget.stream = s
                widget.channel = channel
            item.setExpanded(not s.name.endswith('_raw'))
            self.addTopLevelItem(item)



class SensorGraph(plotwidget.PlotWidget):
    def __init__(self, parser, parent=None):
        super().__init__(parent)
        self.graphs = {}
        streams = stream.Stream.getInstances()
        for i, s in enumerate(streams):
            for channel in s:
                graph = streamGraph(self.figure.axes[0], s, channel)
                graph.setVisible(False)
                self.graphs[s.name + '.' + channel] = graph
        parser.nextIteration.connect(self.replot)


class SensorGraphWidget(QtGui.QWidget):
    def __init__(self, estimator, parent=None):
        super().__init__(parent)

        self.parser = parser
        self.sensorTree = SensorTreeWidget()
        self.sensorTree.setMaximumWidth(200)
        self.sensorTree.selectionModel().selectionChanged.connect(self.selectionChanged)
        self.recordButton = QtGui.QPushButton('record')
        self.recordButton.clicked.connect(self.record)
        self.graph = SensorGraph(estimator.thread)

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
                graphs.append(self.graph.graphs[widget.stream.name + '.' + widget.channel])
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
    from processing import estimator

    est= estimator.Estimator()

    app = QtGui.QApplication(sys.argv)
    widget = SensorGraphWidget(est)
    widget.show()
    sys.exit(app.exec_())
