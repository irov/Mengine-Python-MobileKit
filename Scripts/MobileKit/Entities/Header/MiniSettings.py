from Foundation.TaskManager import TaskManager
from MobileKit.HeaderComponent import HeaderComponent
from MobileKit.PrototypeManager import PrototypeManager


class MiniSettings(HeaderComponent):

    """ Parent class for own MiniSettings """

    def __init__(self):
        super(MiniSettings, self).__init__()
        self.movie = None
        self.tc = None

    def _onPreparation(self):
        if self.header.movie_content.hasMovieSlot("settings") is False:
            Trace.log("HeaderComponent", 0, "Not found slot 'settings' in header")
            return

        slot = self.header.movie_content.getMovieSlot("settings")
        self.movie = PrototypeManager.generateObjectUniqueOnNode(slot, "MiniSettings")

    def _onActivate(self):
        if self.movie is None:
            return

        if self._checkIfAllowed() is False:
            self.movie.setEnable(True)

        self.tc = TaskManager.createTaskChain(Name="Header_Settings", Repeat=True)
        with self.tc as tc:
            tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.movie, SocketName="socket")
            tc.addScope(self._scopeOpenSettings)

    def _onFinalize(self):
        if self.tc is not None:
            self.tc.cancel()
            self.tc = None

        super(MiniSettings, self)._onFinalize()

        if self.movie is not None:
            self.movie.onDestroy()
            self.movie = None

    def _scopeOpenSettings(self, source):
        raise NotImplementedError()

    def _checkIfAllowed(self):
        return True
