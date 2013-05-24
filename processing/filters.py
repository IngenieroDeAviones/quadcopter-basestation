
import stream


class Filter(stream.Stream):
    def __init__(self, inputStream, channels=None, name=None, parent=None):
        print(channels, inputStream)
        name = str(name) if not name is None else 'filter.' + self.__class__.__name__
        super().__init__(channels=channels or inputStream, name=name, parent=parent)
        if inputStream:
            self.inputStream = inputStream
            self.inputStream.updated.connect(self.newData)


    def newData(self, stream):
        self.update(stream._channels)


class LowPass(Filter):
    def __init__(self, inputStream, tau, name=None, parent=None):
        super().__init__(inputStream, name, parent)
        self.tau = tau


    def newData(self, stream):
        try:
            a = 1 / (1 + self.tau)
            d = {}
            for channel, value in self.items():
                d[channel] = value + a * (stream[channel] - value)
                #y[i-1] + α * (x[i] - y[i-1])
            self.update(d)
        except:
            self.update(stream._channels)


class HighPass(Filter):
    def __init__(self, inputStream, tau, name=None, parent=None):
        super().__init__(inputStream, name, parent)
        self.tau = tau
        self.x_last = None


    def newData(self, stream):
        if self.x_last:
            a = 1 / (1 + self.tau)
            d = {}
            for channel, value in self.items():
                d[channel] = a * (value + stream[channel] - self.x_last[channel])
                #y[i] := α * (y[i-1] + x[i] - x[i-1])
            self.update(d)
        else:
            self.update(stream._channels)
        self.x_last = stream._channels.copy()


class Integrator(Filter):
    def newData(self, stream):
        try:
            dt = stream.dt.total_seconds
            self.update({channel: value + stream[channel] * dt for channel, value in self._channels.items()})
        except:
            self.update(stream._channels)
    

class Sum(Filter):
    def __init__(self, inputStreams, channels=None, name=None, parent=None):
        super().__init__(None, name=name, parent=parent, channels = channels or inputStreams[0])
        self.inputStreams = inputStreams
        for stream in self.inputStreams:
            stream.updated.connect(self.newData)


    def newData(self, stream):
        #HACK: fix filters to allow for different channel names
        self.update({channel: sum([list(stream._channels.values())[i] for stream in self.inputStreams]) for i, channel in enumerate(self.inputStreams[0])})
        #self.update({channel: sum([stream[channel] for stream in self.inputStreams]) for channel in self._channels})



class Complementary(Sum):
    def __init__(self, inputProportional, inputDifferential, tau, name=None, parent=None):
        self.inputProportional = inputProportional
        self.lowpass = LowPass(self.inputProportional, tau)
        self.lowpass.updated.connect(self.newData)

        self.inputDifferential = inputDifferential
        self.highpass = HighPass(self.inputDifferential, tau)
        self.integrator = Integrator(self.highpass)
        self.integrator.updated.connect(self.newData)

        super().__init__([self.lowpass, self.integrator], name=name, parent=parent)
