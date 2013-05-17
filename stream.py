#! /usr/bin/env python3

from collections import OrderedDict, defaultdict
import datetime
import weakref
from PyQt4 import QtCore

class Stream(QtCore.QObject):
    """Class representing a data stream.
    
    A stream can have multiple channels. Each time a channel value is updated
    the updated signal is emitted.
    
    """
    updated = QtCore.pyqtSignal(QtCore.QObject)
    __refs__ = []


    def __init__(self, channels=None, name=None, parent=None):
        super().__init__(parent)
        self.__refs__.append(weakref.ref(self))
        self._channels = OrderedDict()
        self.timestamp = datetime.datetime.now()
        self.name = str(name) if not name is None else self.__class__.__name__
        self._channels.update(zip(channels, (None, ) * len(channels)))


    def update(self, values):
        """Update one or more channel values."""
        if not isinstance(values, dict):
            values = {channel: value for channel, value in zip(self._channels, values)}
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


    @classmethod
    def getInstances(cls):
        for ref in cls.__refs__:
            instance = ref()
            if instance is not None:
                 yield instance
