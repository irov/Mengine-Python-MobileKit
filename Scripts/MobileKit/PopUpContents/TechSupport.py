from MobileKit.PopUpContent import PopUpContent
from MobileKit.PrototypeManager import PrototypeManager

BUILD_VERSION_BOOL = Mengine.getGameParamBool("ShowBuildVersion", True)
PLAYFAB_ID_BOOL = Mengine.getGameParamBool("ShowPlayFabId", True)


class TechSupport(PopUpContent):
    popup_id = "tech_support"
    title_text_id = "ID_PopUp_TechSupport"
    content_movie_name = "Movie2_Content_TechSupport"

    def __init__(self):
        super(TechSupport, self).__init__()
        self.movies = {}
        self.buttons = {}

    def _onInitialize(self):
        return

    def _onPreparation(self):
        def _attachTo(slot, obj):
            if self._checkSlot(slot) is False:
                return False
            slot_obj = self.content.getMovieSlot(slot)
            node = obj.getEntityNode()
            slot_obj.addChild(node)

        if self.content.hasSlot("send_mail") is True:
            self.buttons["send_mail"] = PrototypeManager.generateObjectContainer("Button")
            self.buttons["send_mail"].setTextAliasEnvironment("contact_us")
            _attachTo("send_mail", self.buttons["send_mail"])
            self.buttons["send_mail"].setEnable(True)

        # initialize build version and playfab id
        if BUILD_VERSION_BOOL is True:
            build_version = PrototypeManager.generateObjectUnique("Build_Version")
            build_version.setEnable(True)
            _attachTo("build_version", build_version)
            self.movies["build_version"] = build_version

        if PLAYFAB_ID_BOOL is True:
            playfab_id = PrototypeManager.generateObjectUnique("PlayFab_Id")
            playfab_id.setEnable(True)
            _attachTo("playfab_id", playfab_id)
            self.movies["playfab_id"] = playfab_id

    def _onActivate(self):
        self.content.setEnable(True)

        if self.buttons["send_mail"] is not None:
            with self.createTaskChain("send_mail") as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.buttons["send_mail"].movie)
                tc.addScope(self._scopeBugReport)

    def _onDeactivate(self):
        self.content.setEnable(False)

    def _onFinalize(self):
        for movie in self.movies.values():
            movie.onDestroy()
        self.movies = {}

        for btn in self.buttons.values():
            btn.onDestroy()
        self.buttons = {}

    # utils
    def _checkSlot(self, slot_name):
        if self.content.hasSlot(slot_name) is False:
            Trace.log("Entity", 0, "Slot {!r} not found in {!r}".format(slot_name, self.content.getName()))
            return False

        return True

    # -- Contact us button

    def _scopeBugReport(self, source):
        source.addDelay(300)
        source.addFunction(self.sendSupportMail)

    def sendSupportMail(self):
        receiver = Mengine.getGameParamUnicode("TechnicalSupportEmail")
        subject = u"[{}] Technical Support Request".format(Mengine.getProjectName())
        body = self.getSupportMessageBody()

        if _DEVELOPMENT is True:
            Trace.msg("DUMMY send support mail:\n  Receiver: {!r}\n  Subject: {!r}"
                      "\n{}\n  (Include player save)".format(receiver, subject, body))

        Mengine.openMail(receiver, subject, body)

    # todo for @eclipse7723: make it as a template in Foundation for all projects
    def getSupportMessageBody(self):
        mode = "dev" if _DEVELOPMENT is True else "master"
        playfab_id = str(Mengine.getCurrentAccountSetting("PlayFabId"))

        kwargs = dict(
            BUILD_VERSION=_BUILD_VERSION,
            BUILD_VERSION_NUMBER=_BUILD_VERSION_NUMBER,
            BUILD_VERSION_CODE=_BUILD_VERSION,
            PLAYFAB_ID=playfab_id,
            OS_NAME=Utils.getCurrentPlatform(),
            OS_VERSION="unknown",
            PLAYFAB_REVISION_MODE=mode,
        )
        if _ANDROID:
            kwargs["OS_VERSION"] = Mengine.androidStringMethod("Application", "getOSVersion")
            kwargs["BUILD_VERSION_CODE"] = Mengine.androidIntegerMethod("Application", "getVersionCode")

        body = u"""

----- Please Describe Your Issue Above Here -----

        Important Details for our Support Team:
        * build version: {BUILD_VERSION} ({BUILD_VERSION_NUMBER})
        * version code: {BUILD_VERSION_CODE}
        * playfab id: {PLAYFAB_ID}
        * playfab revision: {PLAYFAB_REVISION_MODE}
        * {OS_NAME} version: {OS_VERSION}
        """.format(**kwargs)

        return body

