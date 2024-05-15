from Foundation.Initializer import Initializer


class HeaderComponent(Initializer):
    
    def __init__(self):
        super(HeaderComponent, self).__init__()
        self.header = None
        self.observers = []

    def _onInitialize(self, header, *args, **kwargs):
        self.header = header
        self._onPreparation(*args, **kwargs)

    def _onPreparation(self, *args, **kwargs):
        pass

    def onActivate(self):
        self._onActivate()
    
    def _onActivate(self):
        pass

    def _onFinalize(self):
        self.header = None

        for observer in self.observers:
            Notification.removeObserver(observer)
        self.observers = []

    def addObserver(self, identity, cb, *args):
        observer = Notification.addObserver(identity, cb, *args)
        self.observers.append(observer)
