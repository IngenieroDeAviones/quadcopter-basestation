#!/usr/bin/python3

import sys
import math
from PyQt4 import QtGui, QtCore

import os
sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))] + sys.path
import parser
from processing import estimator
from sensors import sensor
from widgets import gridlayout, debug
from widgets.instruments import compass, altimeter, horizon, current, temperature

class MainPanel(QtGui.QMainWindow):
   
    def __init__(self):
        super(MainPanel, self).__init__()

        self.resize(900, 620)
        self.centralWidget = CentralWidget(self)
        self.menuBar = MenuBar(self)
        self.setWindowTitle('Main panel')

class MenuBar(QtGui.QMenuBar):

    def __init__(self, parent):
        super(MenuBar, self).__init__(parent)

        # Define actions

        # File menu
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        # View menu
        showAltimeter = QtGui.QAction(parent)
        showAltimeter.setCheckable(True)
        showAltimeter.setChecked(True)
        showAltimeter.setObjectName("Altimeter")
        showAltimeter.setText("&Altimeter")
        showAltimeter.toggled.connect(parent.centralWidget.instruments['altimeter'].setVisible)

        showCompass = QtGui.QAction(self)
        showCompass.setCheckable(True)
        showCompass.setChecked(True)
        showCompass.setObjectName("Compass")
        showCompass.setText("&Compass")
        showCompass.toggled.connect(parent.centralWidget.instruments['compass'].setVisible)

        showHorizon = QtGui.QAction(parent)
        showHorizon.setCheckable(True)
        showHorizon.setChecked(True)
        showHorizon.setObjectName("Horizon")
        showHorizon.setText("&Horizon")
        showHorizon.toggled.connect(parent.centralWidget.instruments['horizon'].setVisible)

        editMode = QtGui.QAction(parent)
        editMode.setCheckable(True)
        editMode.setText("&Edit Layout")
        editMode.toggled.connect(parent.centralWidget.enterEditMode)

        showDebugAction = QtGui.QAction(parent)
        showDebugAction.setText('Show &Debug Window')
        showDebugAction.triggered.connect(self.openDebugWindow)

        # Add menuBar to mainPanel
        menubar = parent.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(showAltimeter)
        viewMenu.addAction(showCompass)
        viewMenu.addAction(showHorizon)
        viewMenu.addSeparator()
        viewMenu.addAction(editMode)

        debugMenu = menubar.addMenu('&Debug')
        debugMenu.addAction(showDebugAction)


    def openDebugWindow(self, centralWidget):
        if not hasattr(self, 'debugWindow'):
            self.debugWindow = debug.DebugWindow(self.parent().centralWidget.estimator.sensors.thread)
        self.debugWindow.show()


class CentralWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(CentralWidget, self).__init__(parent)

        self.estimator = estimator.Estimator(sensor.SensorManager())

        self.layout = gridlayout.GridLayout([12, 8])

        self.instruments = {}
        self.instruments['compass'] = compass.CompassWidget(self.estimator, self)
        self.instruments['compass'].setSpan(4)
        self.instruments['altimeter'] = altimeter.AltimeterWidget(None, self)
        self.instruments['altimeter'].setSpan(4)
        self.instruments['horizon'] = horizon.HorizonWidget(self.estimator, self)
        self.instruments['horizon'].setSpan(4)

        for i in range(1,5):
            name = 'Current' + str(i)
            self.instruments[name] = current.CurrentWidget(parent=self)
            self.instruments[name].setSpan(2)

            name = 'Temperature' + str(i)
            self.instruments[name] = temperature.TemperatureWidget(parent=self)
            self.instruments[name].setSpan(2)

        self.layout.addWidget(self.instruments['compass'], 0, 0)
        self.layout.addWidget(self.instruments['altimeter'], 4, 0)
        self.layout.addWidget(self.instruments['horizon'], 8, 0)
        self.layout.addWidget(self.instruments['Current1'], 0, 4)
        self.layout.addWidget(self.instruments['Current2'], 2, 4)
        self.layout.addWidget(self.instruments['Current3'], 2, 6)
        self.layout.addWidget(self.instruments['Current4'], 0, 6)
        self.layout.addWidget(self.instruments['Temperature1'], 4, 4)
        self.layout.addWidget(self.instruments['Temperature2'], 6, 4)
        self.layout.addWidget(self.instruments['Temperature3'], 6, 6)
        self.layout.addWidget(self.instruments['Temperature4'], 4, 6)

        # Add centralWidget to mainPanel
        parent.setCentralWidget(self)

        self.setLayout(self.layout)

#    def minimumHeightForWidth(self,w):
#        return w*5/9


    def enterEditMode(self, editMode):
        for instrument in self.instruments.values():
            if editMode:
                instrument.enterLayoutEditMode()
            else:
                instrument.exitLayoutEditMode()


#    def resizeEvent(self, event):
#       size = min(event.width / self.columnCount, event.height / self.rowCount)
#
#        for column in self.columnCount:
#            self.layout

def main():

    app = QtGui.QApplication(sys.argv)
    mainpanel = MainPanel()
    mainpanel.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
