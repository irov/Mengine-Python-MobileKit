from MobileKit.PopUpContent import PopUpContent
from MobileKit.PrototypeManager import PrototypeManager
from MobileKit.CreditsManager import CreditsManager
from MobileKit.AdjustableScreenUtils import AdjustableScreenUtils


class Credits(PopUpContent):
    popup_id = "credits"
    title_text_id = "ID_PopUp_Credits"
    content_movie_name = "Movie2_Content_Credits"

    def __init__(self):
        super(Credits, self).__init__()

    def _onInitialize(self):
        return

    def _onPreparation(self):
        if self.content is None:
            return

        if self.content.hasSlot("data") is False:
            return False
        slot = self.content.getMovieSlot("data")

        viewport = Mengine.getGameViewport()
        game_width, game_height, top_offset, bottom_offset = AdjustableScreenUtils.getMainSizes()

        x_center = viewport.begin.x + game_width / 2
        y_center = viewport.begin.y + game_height / 2

        slot.setWorldPosition(Mengine.vec2f(x_center,  viewport.begin.y))

        for param in CreditsManager.getParams():

            credit_object = PrototypeManager.generateObjectUnique(param.Movie2Prototype[7:])
            credit_object.setEnable(True)

            node = credit_object.getEntityNode()
            node.removeFromParent()
            slot.addChild(node)

            credit_object.setPosition((0, param.OffsetTop))

    def _onActivate(self):
        self.content.setEnable(True)

    def _onDeactivate(self):
        self.content.setEnable(False)

    def _onFinalize(self):
        return
