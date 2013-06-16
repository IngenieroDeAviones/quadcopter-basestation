#!/usr/bin/python3

import sys
import math
from PyQt4 import QtGui, QtCore

import os
sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))] + sys.path
import parser
from processing import estimator
from widgets import floatlayout
from widgets.instruments import compass, altimeter, horizon

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
        showAltimeter.toggled.connect(parent.centralWidget.instruments['altimeter'].setVisible)

        showCompass = QtGui.QAction(parent)
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


class CentralWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(CentralWidget, self).__init__(parent)

        self.estimator = estimator.Estimator()

        self.layout = floatlayout.FloatLayout([9, 5], parent=self)

        self.instruments = {}
        self.instruments['compass'] = compass.CompassWidget(self.estimator, self)
        self.instruments['altimeter'] = altimeter.AltimeterWidget(None, self)
        self.instruments['horizon'] = horizon.HorizonWidget(self.estimator, self)

        self.layout.addWidget(self.instruments['compass'])
        self.layout.addWidget(self.instruments['altimeter'])
        self.layout.addWidget(self.instruments['horizon'])

        # Add centralWidget to mainPanel
        parent.setCentralWidget(self)

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
