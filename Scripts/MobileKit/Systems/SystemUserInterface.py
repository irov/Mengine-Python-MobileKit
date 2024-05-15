from Foundation.System import System


class SystemUserInterface(System):

    """ parent for Game.Systems.SystemUserInterface """

    def __init__(self):
        super(SystemUserInterface, self).__init__()

    def _onInitialize(self):
        pass

    def _onRun(self):
        self.addObserver(Notificator.onRun, self._cbRun)
        return True

    def _onStop(self):
        pass

    def _onFinalize(self):
        pass

    # observers

    def _cbRun(self):
        self._setTexts()
        return True

    # utils

    def _setTexts(self):
        return
