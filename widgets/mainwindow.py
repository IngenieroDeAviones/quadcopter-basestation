#!/usr/bin/python3

import sys
import math
from PyQt4 import QtGui, QtCore
from instruments import compass, altimeter, horizon

class MainPanel(QtGui.QMainWindow):
   
    def __init__(self):
        super(MainPanel, self).__init__()

        self.resize(1080, 380)

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
        showAltimeter.toggled.connect(parent.centralWidget.altimeter.setVisible)

        showCompass = QtGui.QAction(parent)
        showCompass.setCheckable(True)
        showCompass.setChecked(True)
        showCompass.setObjectName("Compass")
        showCompass.setText("&Compass")
        showCompass.toggled.connect(parent.centralWidget.compass.setVisible)

        showHorizon = QtGui.QAction(parent)
        showHorizon.setCheckable(True)
        showHorizon.setChecked(True)
        showHorizon.setObjectName("Horizon")
        showHorizon.setText("&Horizon")
        showHorizon.toggled.connect(parent.centralWidget.horizon.setVisible)

        # Add menuBar to mainPanel
        menubar = parent.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(showAltimeter)
        viewMenu.addAction(showCompass)
        viewMenu.addAction(showHorizon)        

class CentralWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(CentralWidget, self).__init__(parent)

        self.layout = QtGui.QGridLayout(self)

        self.compass = compass.CompassWidget()
        self.altimeter = altimeter.AltimeterWidget()
        self.horizon = horizon.HorizonWidget()

        # Add widgets to centralWidget        
        self.layout.addWidget(self.compass, 0, 0)
        self.layout.addWidget(self.altimeter, 0, 1)
        self.layout.addWidget(self.horizon, 0, 2)

        # Add centralWidget to mainPanel
        parent.setCentralWidget(self)


def main():

    app = QtGui.QApplication(sys.argv)
    mainpanel = MainPanel()
    mainpanel.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
