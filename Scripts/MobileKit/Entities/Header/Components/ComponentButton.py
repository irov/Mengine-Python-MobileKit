from MobileKit.HeaderComponent import HeaderComponent
from MobileKit.PrototypeManager import PrototypeManager


class ComponentButton(HeaderComponent):
    slot_name = None
    prototype_name = None

    def __init__(self):
        super(ComponentButton, self).__init__()
        self.movie = None

    def _onPreparation(self):
        if self.header.movie_content.hasMovieSlot(self.slot_name) is False:
            Trace.log("HeaderComponent", 0, "Not found slot {!r} in Header!".format(self.slot_name))
            return

        slot = self.header.movie_content.getMovieSlot(self.slot_name)
        self.movie = PrototypeManager.generateObjectUniqueOnNode(slot, self.prototype_name)

    def _onActivate(self):
        if self.movie is None:
            return

        if self._checkIfAllowed() is True:
            self.movie.setEnable(True)

        self._runTaskChains()

    def _runTaskChains(self):
        tc_name = "{}_{}".format(self.header.__class__.__name__, self.__class__.__name__)
        with self._createTaskChain(tc_name, Repeat=True) as tc:
            tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.movie, SocketName="socket")
            tc.addScope(self._scopeComponentLogic)

    def _checkIfAllowed(self):
        return True

    def _scopeComponentLogic(self, source):
        raise NotImplementedError()

    def _onFinalize(self):
        super(ComponentButton, self)._onFinalize()
        if self.movie is not None:
            self.movie.onDestroy()
            self.movie = None

        self.prototype_name = None
        self.slot_name = None
