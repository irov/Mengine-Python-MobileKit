from MobileKit.PopUpContent import PopUpContent
from MobileKit.AdjustableScreenUtils import AdjustableScreenUtils
# todo: from Foundation.LanguagesManager import LanguagesManager
from Foundation.SystemManager import SystemManager
from Foundation.TaskManager import TaskManager
from Foundation.DefaultManager import DefaultManager

ALIAS_BUTTON_IDLE = "$AliasButtonLangIdle"
ALIAS_BUTTON_BLOCK = "$AliasButtonLangBlock"

SLOT_LANG = "lang"
BUTTON_PROTOTYPE = "Movie2Button_Language"

COLOR_DARK_GRAY = (0.84, 0.84, 0.84, 1.0)
COLOR_LIGHT_GRAY = (0.25, 0.24, 0.24, 1.0)


class Languages(PopUpContent):

    popup_id = "languages"
    title_text_id = "ID_PopUp_Language"
    content_movie_name = "Movie2_Content_Language"

    def __init__(self):
        super(Languages, self).__init__()
        self.content = None
        self.tcs = []

        self.buttons_lang = {}
        self.buttons_list = []

        self._color_text_button_idle = None
        self._color_text_button_block = None

        self._offset_top = None
        self._offset_x = None
        self._offset_y = None

    def _onInitialize(self):
        self._color_text_button_idle = DefaultManager.getDefaultTuple("PopUpLanguagesColorTextButtonIdle", COLOR_DARK_GRAY)
        self._color_text_button_block = DefaultManager.getDefaultTuple("PopUpLanguagesColorTextButtonBlock", COLOR_LIGHT_GRAY)

        self._offset_top = DefaultManager.getDefaultFloat("LanguagesOffsetTop", 100.0)
        self._offset_x = DefaultManager.getDefaultFloat("LanguagesOffsetX", 245.0)
        self._offset_y = DefaultManager.getDefaultFloat("LanguagesOffsetY", 180.0)

    def _onPreparation(self):
        if self.content is None:
            return

        self._generateLangButtons()
        self._setButtonsPosition()

    def _onActivate(self):
        self.content.setEnable(True)

        if len(self.buttons_lang) != 0:
            with self._createTaskChain(SLOT_LANG) as tc:
                for (lang, button), tc_race in tc.addRaceTaskList(self.buttons_lang.items()):
                    tc_race.addTask("TaskMovie2ButtonClick", Movie2Button=button)
                    tc_race.addFunction(self._changeLocale, lang)

    def _onDeactivate(self):
        self.content.setEnable(False)

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

    def _onFinalize(self):
        self.content = None

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        for button in self.buttons_lang.values():
            button.onDestroy()
        self.buttons_lang = {}
        self.buttons_list = []

    def _createTaskChain(self, name, **params):
        tc = TaskManager.createTaskChain(Name="Stats_"+name, **params)
        self.tcs.append(tc)
        return tc

    def _generateLangButtons(self):
        if self._checkSlot(SLOT_LANG) is False:
            return

        def _generateButton(text_id):
            env = BUTTON_PROTOTYPE + "_" + lang
            button = self.owner.object.tryGenerateObjectUnique(env, BUTTON_PROTOTYPE)
            button.setTextAliasEnvironment(env)

            for movie in button.eachMovies():
                if movie.setupMovieTextColor(ALIAS_BUTTON_IDLE, self._color_text_button_idle) is True:
                    Mengine.setTextAlias(env, ALIAS_BUTTON_IDLE, text_id)

                elif movie.setupMovieTextColor(ALIAS_BUTTON_BLOCK, self._color_text_button_block) is True:
                    Mengine.setTextAlias(env, ALIAS_BUTTON_BLOCK, text_id)

                else:
                    Trace.log("PopUp", 0, "[Languages] button movie state {!r} should have {!r} or {!r} text aliases"
                              .format(movie.name, ALIAS_BUTTON_IDLE, ALIAS_BUTTON_BLOCK))

            button.setEnable(True)
            return button

        slot_lang_start = self.content.getMovieSlot(SLOT_LANG)
        _, _, top_offset, _, viewport, x_center, _ = AdjustableScreenUtils.getMainSizesExt()
        slot_lang_start.setWorldPosition(Mengine.vec2f(x_center, viewport.begin.y + top_offset + self._offset_top))

        try:
            from Game.LanguagesManager import LanguagesManager   # fixme
        except ImportError:
            Trace.log("PopUp", 0, "Not found module Game.LanguagesManager (fixme)")
            return

        lang_params = LanguagesManager.getParams()

        for param in lang_params:
            text, lang = param.get()

            btn_lang_obj = _generateButton(text)
            btn_lang_obj_node = btn_lang_obj.getEntityNode()
            slot_lang_start.addChild(btn_lang_obj_node)

            if Mengine.getLocale() == lang:
                btn_lang_obj.setBlock(True)

            self.buttons_lang[lang] = btn_lang_obj
            self.buttons_list.append(btn_lang_obj)

    def _setButtonsPosition(self):
        # Buttons start local pos
        button_pos_x, button_pos_y = 0.0, 500.0
        i = 0
        offset_y_temp = 0

        for button in self.buttons_list:
            i += 1
            button_pos_y += offset_y_temp

            if i % 2 != 0:
                button_pos_x -= self._offset_x
            else:
                button_pos_x += self._offset_x
                offset_y_temp += self._offset_y

            button_node = button.getEntityNode()
            button_node.setLocalPosition((button_pos_x, button_pos_y))

            button_pos_x, button_pos_y = 0.0, 500.0

    def _changeLocale(self, locale):
        if SystemManager.hasSystem("SystemAutoLanguage"):
            Mengine.changeCurrentAccountSetting("SelectedLanguage", unicode(locale))
            SystemManager.getSystem("SystemAutoLanguage").disable()

        def cbOnSceneRestartChangeLocale(scene, isActive, isError):
            if scene is None:
                Mengine.setLocale(locale)

        Mengine.restartCurrentScene(True, cbOnSceneRestartChangeLocale)

    def _checkSlot(self, slot_name):
        if self.content.hasSlot(slot_name) is False:
            Trace.log("PopUp", 0, "Slot {!r} not found in {!r}".format(slot_name, self.content.getName()))
            return False

        return True
