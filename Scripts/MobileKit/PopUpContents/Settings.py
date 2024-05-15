from Foundation.TaskManager import TaskManager
from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from MobileKit.AdjustableScreenUtils import AdjustableScreenUtils
from MobileKit.PopUpContent import PopUpContent
from MobileKit.PrototypeManager import PrototypeManager
from Game.PopUpContents.Languages import Languages


class Settings(PopUpContent):
    popup_id = "settings"
    title_text_id = "ID_PopUp_Settings"

    def __init__(self):
        super(Settings, self).__init__()
        self.tcs = []
        self.buttons = {}
        self.checkboxes = {}

    def _onInitialize(self):
        self.content = self.owner.object.getObject("Movie2_Content_Settings")

        if self.content is None:
            Trace.log("Entity", 0, "Not found Movie2_Content in Settings")
            return

    def _onPreparation(self):
        if self.content is None:
            return

        def _generateButton(name, env):
            button = PrototypeManager.generateObjectContainer(name)
            button.setTextAliasEnvironment(env)
            button.setEnable(True)
            return button

        # buttons
        if self.content.hasSlot("language") is True:
            self.buttons["language"] = _generateButton("Button", "language")
            Languages.setBtnCurrentLocale()

        if self.content.hasSlot("credits") is True:
            self.buttons["credits"] = _generateButton("Button", "credits")
        if self.content.hasSlot("terms") is True:
            self.buttons["terms"] = _generateButton("Button", "terms")
        if self.content.hasSlot("techsupport") is True:
            self.buttons["techsupport"] = _generateButton("Button", "techsupport")

        # checkboxes
        if self.content.hasSlot("sound"):
            self.checkboxes["sound"] = self.owner.object.getObject("Movie2CheckBox_MuteSound")
            self.checkboxes["sound"].setParam("Value", self._getMuteSoundSetting())

        if self.content.hasSlot("music"):
            self.checkboxes["music"] = self.owner.object.getObject("Movie2CheckBox_MuteMusic")
            self.checkboxes["music"].setParam("Value", self._getMuteMusicSetting())

        # attach to slots
        for slot_name, movie in self.__getAllObjects():
            if self.content.hasSlot(slot_name) is False:
                Trace.log("Entity", 0, "Slot {!r} not found in {!r}".format(slot_name, self.content.getName()))
                continue

            slot = self.content.getMovieSlot(slot_name)
            node = movie.getEntityNode()
            node.removeFromParent()
            slot.addChild(node)

            movie.setEnable(True)

        self.__adjustSlotsPosition()

    def _onActivate(self):
        self.content.setEnable(True)

        if self.checkboxes.get("sound") is not None:
            checkbox_sound = self.checkboxes["sound"]

            with self._createTaskChain("MuteSound", Repeat=True) as tc:
                with tc.addRaceTask(2) as (true, false):
                    true.addTask("TaskMovie2CheckBox", Movie2CheckBox=checkbox_sound, Value=True)
                    true.addScope(self._scopeMuteSoundHandler, checkbox_sound, True)

                    false.addTask("TaskMovie2CheckBox", Movie2CheckBox=checkbox_sound, Value=False)
                    false.addScope(self._scopeMuteSoundHandler, checkbox_sound, False)

        if self.checkboxes.get("music") is not None:
            checkbox_music = self.checkboxes["music"]

            with self._createTaskChain("MuteMusic", Repeat=True) as tc:
                with tc.addRaceTask(2) as (true, false):
                    true.addTask("TaskMovie2CheckBox", Movie2CheckBox=checkbox_music, Value=True)
                    true.addScope(self._scopeMuteMusicHandler, checkbox_music, True)

                    false.addTask("TaskMovie2CheckBox", Movie2CheckBox=checkbox_music, Value=False)
                    false.addScope(self._scopeMuteMusicHandler, checkbox_music, False)

        if self.buttons["language"] is not None:
            with self._createTaskChain("Languages", Repeat=True) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.buttons["language"].movie)
                tc.addScope(self._scopeLanguage)

        if self.buttons["credits"] is not None:
            with self._createTaskChain("Credits", Repeat=True) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.buttons["credits"].movie)
                tc.addScope(self._scopeCredits)

        if self.buttons["techsupport"] is not None:
            with self._createTaskChain("TechSupport", Repeat=True) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.buttons["techsupport"].movie)
                tc.addScope(self._scopeTechSupport)

        if self.buttons["terms"] is not None:
            with self._createTaskChain("ConsentFlow", Repeat=True) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.buttons["terms"].movie)
                tc.addScope(self._scopeConsentSettingsButton)

    def _onDeactivate(self):
        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        self.content.setEnable(False)

    def _onFinalize(self):
        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        for button in self.buttons.values():
            button.onDestroy()
        self.buttons = {}

        for checkbox in self.checkboxes.values():
            checkbox.returnToParent()
        self.checkboxes = {}

        self.content = None

    def __adjustSlotsPosition(self):
        viewport = Mengine.getGameViewport()
        game_width, game_height, top_offset, bottom_offset = AdjustableScreenUtils.getMainSizes()

        x_center = viewport.begin.x + game_width / 2
        y_center = viewport.begin.y + game_height / 2

        # transitions
        y_bottom_transitions = viewport.end.y - bottom_offset - game_height * 0.22
        transition_height = 150.0

        for i, button_name in enumerate(["terms",  "credits", "techsupport", "language"]):
            if self.content.hasSlot(button_name):
                slot = self.content.getMovieSlot(button_name)
                slot.setWorldPosition(Mengine.vec2f(
                    x_center,
                    y_bottom_transitions - (20 + transition_height) * i
                ))

        left_border_pos = x_center - game_width / 2
        top_border_pos = viewport.begin.y + top_offset * 2

        # checkboxes setup
        checkbox_sector_width = game_width / 2
        checkbox_sector_width_half = checkbox_sector_width / 2

        for i, (checkbox_name, checkbox) in enumerate(self.checkboxes.items()):
            if self.content.hasSlot(checkbox_name) is False:
                continue

            checkbox_pos_x = left_border_pos + checkbox_sector_width_half + (checkbox_sector_width * i)

            if checkbox_pos_x < x_center:
                checkbox_pos_x += 140
            if checkbox_pos_x > x_center:
                checkbox_pos_x -= 140

            slot_checkbox = self.content.getMovieSlot(checkbox_name)
            slot_checkbox.setWorldPosition(Mengine.vec2f(checkbox_pos_x, top_border_pos * 1.55))

    def __getAllObjects(self):
        return self.buttons.items() + self.checkboxes.items()

    def _createTaskChain(self, name, **params):
        tc = TaskManager.createTaskChain(Name="Settings_"+name, **params)
        self.tcs.append(tc)
        return tc

    @staticmethod
    def _getMuteSoundSetting():
        return Mengine.getCurrentAccountSettingBool("MuteSound")

    @staticmethod
    def _getMuteMusicSetting():
        return Mengine.getCurrentAccountSettingBool("MuteMusic")

    # scopes
    def _scopeMuteSoundHandler(self, source, checkbox, value):
        source.addFunction(checkbox.setParam, "Value", value)
        source.addFunction(Mengine.changeCurrentAccountSetting, "MuteSound", unicode(value))

    def _scopeMuteMusicHandler(self, source, checkbox, value):
        source.addFunction(checkbox.setParam, "Value", value)
        source.addFunction(Mengine.changeCurrentAccountSetting, "MuteMusic", unicode(value))

    def _scopeLanguage(self, scope):
        scope.addNotify(Notificator.onPopUpOpen, "languages")

    def _scopeCredits(self, scope):
        scope.addNotify(Notificator.onPopUpOpen, "credits")

    def _scopeTechSupport(self, scope):
        scope.addNotify(Notificator.onPopUpOpen, "tech_support")

    def _scopeConsentSettingsButton(self, source):
        source.addDelay(300)  # fix for part services spamming
        source.addFunction(AdvertisementProvider.showConsentFlow)


