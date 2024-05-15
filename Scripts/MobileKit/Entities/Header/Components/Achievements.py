from Foundation.TaskManager import TaskManager
from Foundation.Providers.AchievementsProvider import AchievementsProvider
from MobileKit.HeaderComponent import HeaderComponent
from MobileKit.PrototypeManager import PrototypeManager


class Achievements(HeaderComponent):

    def __init__(self):
        super(Achievements, self).__init__()
        self.movie = None
        self.tc = None

    def _onPreparation(self):
        if self.header.movie_content.hasMovieSlot("achievements") is False:
            return
        slot = self.header.movie_content.getMovieSlot("achievements")
        self.movie = PrototypeManager.generateObjectUniqueOnNode(slot, "Achievements")

    def _onFinalize(self):
        if self.tc is not None:
            self.tc.cancel()
            self.tc = None

        super(Achievements, self)._onFinalize()

        if self.movie is not None:
            self.movie.onDestroy()
            self.movie = None

    def _onActivate(self):
        if self.movie is None:
            return

        self.movie.setEnable(True)

        self.tc = TaskManager.createTaskChain(Name="Header_Achievements", Repeat=True)
        with self.tc as tc:
            tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.movie, SocketName="socket")
            tc.addScope(self._scopeOpenAchievements)

    def _scopeOpenAchievements(self, source):
        if AchievementsProvider.hasMethod("showAchievements") is False:
            Trace.msg_err("[!] showAchievements impossible to show - provider failed")

        source.addDelay(300)    # fix for part services spamming
        source.addFunction(AchievementsProvider.showAchievements)
