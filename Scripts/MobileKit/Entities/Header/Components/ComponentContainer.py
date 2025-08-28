from MobileKit.HeaderComponent import HeaderComponent
from MobileKit.PrototypeManager import PrototypeManager


class ComponentContainer(HeaderComponent):
    slot_name = None
    prototype_name = None

    def __init__(self):
        super(ComponentContainer, self).__init__()
        self.container = None

    def _onPreparation(self):
        if self.header.movie_content.hasMovieSlot(self.slot_name) is False:
            Trace.log("HeaderComponent", 0, "Not found slot {!r} in Header!".format(self.slot_name))
            return

        slot = self.header.movie_content.getMovieSlot(self.slot_name)
        self.container = PrototypeManager.generateObjectContainerOnNode(slot, self.prototype_name)

    def _onActivate(self):
        if self.container is None:
            return

        if self._checkIfAllowed() is True:
            self.container.setEnable(True)

        self._runTaskChains()

    def _runTaskChains(self):
        tc_name = "{}_{}".format(self.header.__class__.__name__, self.__class__.__name__)
        with self._createTaskChain(tc_name, Repeat=True) as tc:
            tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.container.movie, SocketName="socket")
            tc.addScope(self._scopeComponentLogic)

    def _checkIfAllowed(self):
        return True

    def _scopeComponentLogic(self, source):
        raise NotImplementedError()

    def _onFinalize(self):
        super(ComponentContainer, self)._onFinalize()
        if self.container is not None:
            self.container.onDestroy()
            self.container = None

        self.prototype_name = None
        self.slot_name = None

    def getSize(self):
        if self.container is None:
            return Mengine.vec2f(0.0, 0.0)

        size = self.container.getSize()
        return size
