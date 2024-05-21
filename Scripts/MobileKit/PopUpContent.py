from Foundation.Initializer import Initializer
from Foundation.TaskManager import TaskManager


class PopUpContent(Initializer):
    popup_id = None             # type: str
    title_text_id = None        # type: str
    content_movie_name = None   # type: str

    def __init__(self):
        super(PopUpContent, self).__init__()
        self.content = None
        self._prepared = False
        self._activate = False
        self.owner = None
        self.tcs = []

    def isPrepared(self):
        return self._prepared is True

    def isActivated(self):
        return self._activate is True

    def onInitialize(self, owner):
        self.owner = owner
        self.content = self.owner.object.getObject(self.content_movie_name)

        if self.content is None:
            Trace.log("PopUp", 0, "Not found {!r} in {!r}".format(self.content_movie_name, self.owner.getName()))
            self._initialized = None    # means not initialized yet
            return False

        super(PopUpContent, self).onInitialize()

    def _onInitialize(self):
        """ here we initialize params, prepare to create objects, etc. """
        raise NotImplementedError

    def onPreparation(self):
        if self.isInitialized() is False:
            Trace.log("PopUp", 0, "Content {!r} must be initialized before onPreparation".format(self.__class__.__name__))
            return

        self._onPreparation()
        self._prepared = True

    def _onPreparation(self):
        """ here we create objects that will be used in future """
        raise NotImplementedError

    def onActivate(self):
        if self.isPrepared() is False:
            Trace.log("PopUp", 0, "Content {!r} must be prepared before onActivate".format(self.__class__.__name__))
            return

        self._onActivate()
        self._activate = True

    def _onActivate(self):
        """ here we activate objects (enable, play animations, etc.) and run tasks"""
        raise NotImplementedError

    def onDeactivate(self):
        if self.isActivated() is False:
            Trace.log("PopUp", 0, "Content {!r} must be activated before onDeactivate".format(self.__class__.__name__))
            return

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        self._onDeactivate()
        self._activate = False

    def _onDeactivate(self):
        """ here we deactivate objects (disable, stop animations, etc.) + auto tcs canceling """
        raise NotImplementedError

    def onFinalize(self):
        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        super(PopUpContent, self).onFinalize()
        self.content = None

        self._initialized = None    # allows to initialize again

    def _onFinalize(self):
        """ here we destroy objects that we created in onPreparation if needed + auto tcs canceling """
        raise NotImplementedError

    def createTaskChain(self, name, **params):
        tc = TaskManager.createTaskChain(Name="PopUpContent_"+self.__class__.__name__+"_"+name, **params)
        self.tcs.append(tc)
        return tc
