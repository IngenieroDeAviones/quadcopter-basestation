#! /usr/bin/env python3

from collections import OrderedDict
import datetime
from PyQt4 import QtCore

class Stream(QtCore.QObject):
    """Class representing a data stream.
    
    A stream can have multiple channels. Each time a channel value is updated
    the updated signal is emitted.
    
    """
    updated = QtCore.pyqtSignal(QtCore.QObject)
    _channels = OrderedDict
    timestamp = datetime.datetime.now()


    def __init__(self, parent=None, channels=None):
        super().__init__(parent)
        self._channels.update({channel: None for channel in channels})


    def update(self, values):
        """Update one or more channel values."""
        if not isinstance(values, dict):
            value = {channel: value for channel, value in zip (self._channels, values)}
        self._channels.update(values)
        self.timestamp = datetime.datetime.now()
        self.updated.emit(self)


    def items(self):
        """Return a list of channel names and values"""
        return self._channels.items()


    def __getitem__(self, channel):
        return self._channels[channel]


    def __setitem__(self, channel, value):
        self._channels[channel] = value
        self.timestamp = datetime.datetime.now()
        self.updated.emit(self)


    def __iter__(self):
        return iter(self._channels)
