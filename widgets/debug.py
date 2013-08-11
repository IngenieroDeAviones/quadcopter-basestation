import struct
from PyQt4 import QtCore, QtGui

import os
import sys
sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))] + sys.path

class DebugWindow(QtGui.QDialog):
    def __init__(self, parser, parent=None):
        super().__init__(parent)

        self.parser = parser

        self.commList = QtGui.QTextEdit()
        self.commList.setReadOnly(True)
        self.parser.commandRecieved.connect(self.commandRecieved)

        self.commandEdit = QtGui.QLineEdit()
        self.sendButton = QtGui.QPushButton('Send')
        self.sendButton.clicked.connect(self.sendCommand)


        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(self.commandEdit)
        hlayout.addWidget(self.sendButton)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.commList)
        layout.addLayout(hlayout)

        self.setLayout(layout)

        self.commandEdit.setFocus()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            self.sendCommand()

    def commandRecieved(self, cmd):
        if not cmd[0] & 0b1111 in (0x2, 0x3, 0x4, 0x5):
            self.commList.append(''.join([hex(c)[2:] for c in cmd]))


    def sendCommand(self):
        command = self.commandEdit.text()
        cmd = bytes()
        for i in range(0, len(command), 2):
            cmd += struct.pack('B', int(command[i:i+2], 16))
        self.parser.send(cmd)
