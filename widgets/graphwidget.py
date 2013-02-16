
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from PyQt4 import QtCore, QtGui


class PlotWidget(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        figure = plt.Figure()
        super().__init__(figure)
        self.setParent(parent)
        self.axes = figure.add_subplot(111)
        self.data = []
        self.draw()


    def replot(self):
        self.draw()


    def addGraph(self, x, y):
        self.data.append(self.axis.plot(x,y))
        self.enabled.append(True)
        return len(self.data)


    def enableGraph(self, index, enabled=True):
        self.enabled[index] = enabled



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    widget = PlotWidget()
    widget.show()
    sys.exit(app.exec_())
