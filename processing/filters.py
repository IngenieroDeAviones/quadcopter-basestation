
import stream


class Filter(stream.Stream):
    def __init__(self, inputStream, name=None, parent=None):
        name = str(name) if not name is None else 'filter.' + self.__class__.__name__
        super().__init__(inputStream, name, parent)
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

