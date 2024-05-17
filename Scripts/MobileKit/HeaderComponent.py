from Foundation.Initializer import Initializer
from Foundation.TaskManager import TaskManager


class HeaderComponentValidationException(Exception):
    def __init__(self, initiator_name, description):
        msg = "HeaderComponent {!r} validation failed: {}".format(initiator_name, description)
        super(HeaderComponentValidationException, self).__init__(msg)


class HeaderComponent(Initializer):
    
    def __init__(self):
        super(HeaderComponent, self).__init__()
        self.header = None
        self.observers = []
        self.tcs = []

    def _onInitialize(self, header, *args, **kwargs):
        self.header = header

        self._onValidate(*args, **kwargs)       # return or raise error

        self._onPreparation(*args, **kwargs)

    def validationFailed(self, description):
        raise HeaderComponentValidationException(self.__class__.__name__, description)

    def _onValidate(self, *args, **kwargs):
        """ override and call self.validationFailed(description) to raise error """
        return True

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

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

    def addObserver(self, identity, cb, *args):
        observer = Notification.addObserver(identity, cb, *args)
        self.observers.append(observer)

    def _createTaskChain(self, name, **params):
        tc = TaskManager.createTaskChain(Name=name, **params)
        self.tcs.append(tc)
        return tc

