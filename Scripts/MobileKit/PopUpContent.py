from Foundation.Initializer import Initializer


class PopUpContent(Initializer):
    popup_id = None
    title_text_id = None

    def __init__(self):
        super(PopUpContent, self).__init__()
        self.content = None
        self._prepared = False
        self._activate = False
        self.owner = None

    def isPrepared(self):
        return self._prepared is True

    def isActivated(self):
        return self._activate is True

    def onInitialize(self, owner):
        self.owner = owner
        super(PopUpContent, self).onInitialize()

    def _onInitialize(self):
        """ here we initialize params, prepare to create objects, etc. """
        raise NotImplementedError

    def onPreparation(self):
        self._onPreparation()
        self._prepared = True

    def _onPreparation(self):
        """ here we create objects that will be used in future """
        raise NotImplementedError

    def onActivate(self):
        self._onActivate()
        self._activate = True

    def _onActivate(self):
        """ here we activate objects (enable, play animations, etc.) and run tasks"""
        raise NotImplementedError

    def onDeactivate(self):
        self._onDeactivate()
        self._activate = False

    def _onDeactivate(self):
        """ here we deactivate objects (disable, stop animations, etc.) and cancel tasks here """
        raise NotImplementedError

    def onFinalize(self):
        super(PopUpContent, self).onFinalize()
        self._initialized = None

    def _onFinalize(self):
        """ here we destroy objects that we created in onPreparation if needed """
        raise NotImplementedError
