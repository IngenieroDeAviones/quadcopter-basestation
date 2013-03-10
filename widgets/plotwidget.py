
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from PyQt4 import QtCore, QtGui


class Graph:
    enabled = True
    def __init__(self, axis, x, y):
        self.axis = axis
        self.x = x
        self.y = y
        self.plot = axis.plot(x, y)[0]
        self.visible = True


    def setVisible(self, visible):
        if visible == self.visible:
            return
        self.visible = visible
        if visible:
            self.axis.add_line(self.plot)
        else:
            self.plot.remove()


    def replot(self):
        self.plot.set_xdata(range(len(self.y)))
        self.plot.set_ydata(self.y)


class PlotWidget(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.figure = plt.Figure()
        super().__init__(self.figure)
        self.setParent(parent)
        self.axes = self.figure.add_subplot(111)
        self.graphs = []
        self.draw()


    def replot(self):
        x_bound = [0,10]
        y_bound = [-1,1]
        for graph in self.graphs.values():
            if graph.y and graph.visible:
                x_bound[1] = max(x_bound[1], len(graph.y))
                y_bound[0] = min(y_bound[0], min(graph.y))
                y_bound[1] = max(y_bound[1], max(graph.y))
            graph.replot()
        self.axes.set_xbound([x * 1.1 for x in x_bound])
        self.axes.set_ybound([y * 1.1 for y in y_bound])
        self.draw()


#    def newAxis(self):
#        return self.figure.axes[0].twinx()


    def newGraph(self, x, y, axis=None):
        return Graph(axis or self.figure.axes[0], x, y)



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    widget = PlotWidget()
    x = [0,1,2,3,4]
    y = [2,5,3,6,1]
    g = widget.newGraph(x, y)
    widget.show()
    sys.exit(app.exec_())
