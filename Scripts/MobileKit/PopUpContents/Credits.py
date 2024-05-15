from MobileKit.PopUpContent import PopUpContent
from MobileKit.PrototypeManager import PrototypeManager


class Credits(PopUpContent):
    popup_id = "credits"
    title_text_id = "ID_PopUp_Credits"

    def __init__(self):
        super(Credits, self).__init__()

    def _onInitialize(self):
        self.content = self.owner.object.getObject("Movie2_Content_Credits")

        if self.content is None:
            Trace.log("Entity", 0, "Not found Movie2_Content in Credits")
            return

    def _onPreparation(self):
        if self.content is None:
            return

        if self.content.hasSlot("logo"):
            logo_developer = PrototypeManager.generateObjectUnique("Logo_Developer")
            logo_developer.setEnable(True)

            slot = self.content.getMovieSlot("logo")
            node = logo_developer.getEntityNode()
            node.removeFromParent()
            slot.addChild(node)

    def _onActivate(self):
        self.content.setEnable(True)

    def _onDeactivate(self):
        self.content.setEnable(False)

    def _onFinalize(self):
        self.content = None
