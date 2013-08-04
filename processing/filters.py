
import stream


class Filter(stream.Stream):
    def __init__(self, inputStream, channelTranslation=None, name=None, parent=None):
        name = str(name) if not name is None else 'filter.' + self.__class__.__name__
        super().__init__(channels=channelTranslation.values() if channelTranslation else inputStream, name=name, parent=parent)
        self.channelTranslation = channelTranslation
        if inputStream:
            self.inputStream = inputStream
            self.inputStream.updated.connect(self.newData)


    def newData(self, stream):
        self.update(stream._channels)


    def update(self, values):
        if isinstance(values, dict) and self.channelTranslation:
            values = {self.channelTranslation[channel]: value for channel, value in values.items()}
        super().update(values)
        


class LowPass(Filter):
    def __init__(self, inputStream, tau, name=None, parent=None):
        super().__init__(inputStream, name, parent)
        self.tau = tau
        self.y_last = None


    def newData(self, stream):
        try:
            dt = stream.dt.total_seconds()
            a = dt / (1 + self.tau)
            d = {}
            for channel, value in stream.items():
                d[channel] = self.y_last[channel] + a * (value - self.y_last[channel])
                #y[i-1] + α * (x[i] - y[i-1])
            self.update(d)
            self.y_last = d
        except:
            self.update(stream._channels)


class HighPass(Filter):
    def __init__(self, inputStream, tau, name=None, parent=None):
        super().__init__(inputStream, name, parent)
        self.tau = tau
        self.x_last = None
        self.y_last = None


    def newData(self, stream):
        if self.x_last:
            dt = stream.dt.total_seconds()
            a = dt * self.tau / (1 + self.tau * dt)
            d = {}
            for channel, value in stream.items():
                d[channel] = a * (self.y_last[channel] + value - self.x_last[channel])
                #y[i] := a * (y[i-1] + x[i] - x[i-1])
            self.update(d)
            self.y_last = d
        else:
            self.update(stream._channels)
            self.y_last = stream._channels
        self.x_last = stream._channels.copy()


class Integrator(Filter):
    def __init__(self, inputStream, channelTranslation=None, name=None, parent=None):
        super().__init__(inputStream, channelTranslation=channelTranslation, name=name, parent=parent)
        self.y_last = None


    def newData(self, stream):
        try:
            dt = stream.dt.total_seconds()
            d = {channel: self.y_last[channel] + value * dt for channel, value in stream.items()}
            self.update(d)
            self.y_last = d
        except:
            self.update(stream._channels)
            self.y_last = stream._channels


class Multiply(Filter):
    def __init__(self, inputStream, factor, channelTranslation=None, name=None, parent=None):
        super().__init__(inputStream, channelTranslation=channelTranslation, name=name, parent=parent)
        if isinstance(factor, dict):
            self.factor = factor
        else:
            self.factor = {channel: factor for channel in inputStream}

    def newData(self,stream):
        self.update({channel: value * self.factor[channel] for channel, value in stream.items()})
    

class Sum(Filter):
    def __init__(self, inputStreams, name=None, parent=None):
        super().__init__(inputStreams[0], name=name, parent=parent)
        self.inputStreams = inputStreams
        for stream in self.inputStreams:
            stream.updated.connect(self.newData)


    def newData(self, stream):
        try:
            self.update({channel: sum([stream[channel] for stream in self.inputStreams]) for channel in self._channels})
        except:
            pass



class Complementary(Sum):
    def __init__(self, inputProportional, inputDifferential, tau, name=None, parent=None):
        self.inputProportional = inputProportional
        self.lowpass = LowPass(self.inputProportional, tau)
        self.lowpass.updated.connect(self.newData)

        self.inputDifferential = inputDifferential
        self.integrator = Integrator(self.inputDifferential, channelTranslation={'x': 'roll', 'y': 'pitch', 'z':'heading'})
        self.highpass = HighPass(self.integrator, tau)
        self.invert = Multiply(self.highpass, -1)
        self.invert.updated.connect(self.newData)

        super().__init__([self.lowpass, self.invert], name=name, parent=parent)
