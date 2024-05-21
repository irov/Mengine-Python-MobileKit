from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from MobileKit.PopUpManager import PopUpManager

SLOT_CLOSE = "close"
SLOT_BACK = "back"

POPUP_TITLE_ALIAS = "$AliasPopUpTitle"


class PopUp(BaseEntity):

    def __init__(self):
        super(PopUp, self).__init__()
        self._content = None
        self.contents = {}

        self.tc_buttons = None
        self.buttons = {}

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addActionActivate(Type, "OpenPopUps",
                               Append=PopUp._cbAppendOpenPopUps,
                               Remove=PopUp._cbRemoveOpenPopUps)

    def _cbAppendOpenPopUps(self, index, popup_id):
        # print " [AppendOpenPopUps] index={}, popup_id={!r} OpenPopUps={}".format(index, popup_id, self.OpenPopUps)
        self._update()

        prev_popup_id = self.OpenPopUps[index-1]
        self.contents[prev_popup_id].onDeactivate()

    def _cbRemoveOpenPopUps(self, index, popup_id, old):
        # print " [RemoveOpenPopUps] index={}, popup_id={!r}, old={}, OpenPopUps={}".format(index, popup_id, old, self.OpenPopUps)

        self._update()
        self.contents[popup_id].onDeactivate()

    def _onPreparation(self):
        if self.object.hasObject("Movie2_Content") is False:
            Trace.log("Entity", 0, "Not found Movie2_Content in {!r}".format(self.object.getName()))
            return

        self._content = self.object.getObject("Movie2_Content")
        self._content.setInteractive(True)

        button_close = self.object.tryGenerateObjectUnique("close", "Movie2Button_Close")
        self._attachTo(button_close, SLOT_CLOSE)
        self.buttons["close"] = button_close

        button_back = self.object.tryGenerateObjectUnique("back", "Movie2Button_Back")
        self._attachTo(button_back, SLOT_BACK)
        self.buttons["back"] = button_back

        self._loadContent()
        self._update()

    def _onActivate(self):
        self.tc_buttons = TaskManager.createTaskChain(Name="PopUp_ActionButtons", Repeat=True)
        with self.tc_buttons as tc:
            with tc.addRaceTask(2) as (close, back):
                close.addTask("TaskMovie2ButtonClick", Movie2Button=self.buttons["close"])
                back.addTask("TaskMovie2ButtonClick", Movie2Button=self.buttons["back"])
            tc.addScope(self._scopeCloseLastContent)

    def _onDeactivate(self):
        if self.tc_buttons is not None:
            self.tc_buttons.cancel()
            self.tc_buttons = None

        self._content = None

        for btn in self.buttons.values():
            btn.onDestroy()
        self.buttons = {}

        for popup_content in self.contents.values():
            if popup_content.isActivated() is True:
                popup_content.onDeactivate()
            popup_content.onFinalize()
        self.contents = {}

    # utils

    def _attachTo(self, btn, slot_name):
        slot = self._content.getMovieSlot(slot_name)
        node = btn.getEntityNode()
        slot.addChild(node)

    def getContentBoundingBox(self):
        """ returns bounding box which is used for content positioning """
        bounding_box = self._content.getCompositionBounds()
        return bounding_box

    # view

    def _loadContent(self):
        for popup_id, popup_content in PopUpManager.getAllPopUpContents().items():
            self.contents[popup_id] = popup_content
            popup_content.onInitialize(self)
            popup_content.onPreparation()

    def _update(self):
        self._updateContent()
        self._updateActionButton()
        self._updateTitle()

    def _updateContent(self):
        if len(self.object.getParam("OpenPopUps")) == 0:
            return

        current_popup_id = self.object.getParam("OpenPopUps")[-1]
        popup_content = self.contents[current_popup_id]
        if popup_content.isActivated() is False:
            popup_content.onActivate()

    def _updateActionButton(self):
        open_popups = self.object.getParam("OpenPopUps")
        if len(open_popups) <= 1:   # 0, 1
            self.buttons["close"].setEnable(True)
            self.buttons["back"].setEnable(False)
        else:   # 2+
            self.buttons["back"].setEnable(True)
            self.buttons["close"].setEnable(False)

    def _updateTitle(self):
        open_pop_ups = self.object.getParam("OpenPopUps")

        if len(open_pop_ups) == 0:
            return

        current_popup_id = open_pop_ups[-1]
        current_popup_content = self.contents[current_popup_id]
        Mengine.setTextAlias("", POPUP_TITLE_ALIAS, current_popup_content.title_text_id)

    # scopes

    def _scopeCloseLastContent(self, source):
        open_popups = self.object.getParam("OpenPopUps")
        last_popup_id = open_popups[-1]

        source.addNotify(Notificator.onPopUpClose, last_popup_id)

