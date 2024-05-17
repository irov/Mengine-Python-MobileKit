from MobileKit.PopUpContent import PopUpContent
from MobileKit.PrototypeManager import PrototypeManager
from MobileKit.CreditsManager import CreditsManager
from MobileKit.AdjustableScreenUtils import AdjustableScreenUtils


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

        for param in CreditsManager.getParams():
            group_name, prototype, offset, alias_id, text_id, slot = param.get()

            if self.content.hasSlot(slot):
                credit_object = PrototypeManager.generateObjectUnique(prototype[7:])
                credit_object.setEnable(True)

                slot = self.content.getMovieSlot(slot)
                node = credit_object.getEntityNode()
                node_pos = node.getWorldPosition()
                node.removeFromParent()
                slot.addChild(node)

                self.__adjustSlotPosition(slot, offset, node_pos)

    def _onActivate(self):
        self.content.setEnable(True)

    def _onDeactivate(self):
        self.content.setEnable(False)

    def _onFinalize(self):
        self.content = None

    def __adjustSlotPosition(self, slot, offset, node_pos):
        viewport = Mengine.getGameViewport()
        game_width, game_height, top_offset, bottom_offset = AdjustableScreenUtils.getMainSizes()

        x_center = viewport.begin.x + game_width / 2
        y_center = viewport.begin.y + game_height / 2

        slot.setWorldPosition(Mengine.vec2f(x_center, node_pos[1] + offset))
