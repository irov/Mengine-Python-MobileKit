from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.Providers.AdvertisementProvider import AdvertisementProvider


class AdvertisingScene(BaseEntity):
    def __init__(self):
        super(AdvertisingScene, self).__init__()
        self.tc = None

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        Type.addAction(Type, "NextScene")
        Type.addAction(Type, "CacheNoAds")
        Type.addAction(Type, "Mode")
        Type.addAction(Type, "AdUnitName")

    def _onActivate(self):
        self.__runTaskChain()

    def _onDeactivate(self):
        if self.tc is not None:
            self.tc.cancel()
            self.tc = None

    def __runTaskChain(self):
        self.tc = TaskManager.createTaskChain()

        with self.tc as tc:
            tc.addScope(self._scopeMain)
            tc.addDelay(1)  # necessary for transition
            tc.addFunction(self.object.runNextScene)

    def _scopeMain(self, source):
        source.addPrint("[AdvertisingScene] Mode [{}] AdUnitName [{}] prepared".format(self.Mode, self.AdUnitName))

        if self.Mode == "Interstitial":
            source.addScope(self._scopeInterstitial)
        elif self.Mode == "Rewarded":
            source.addScope(self._scopeRewarded)
        else:
            Trace.log("Entity", 0, "AdvertisingScene: Unknown Mode: {}".format(self.Mode))

    def _scopeRewarded(self, source):
        with source.addParallelTask(2) as (response, request):
            with response.addRaceTask(3) as (response_ok, response_fail, response_skip):
                response_ok.addListener(Notificator.onAdvertRewarded)
                response_fail.addListener(Notificator.onAdvertDisplayFailed)
                response_skip.addListener(Notificator.onAdvertSkipped)
            request.addFunction(AdvertisementProvider.showAdvert, "Rewarded", self.AdUnitName)

    def _scopeInterstitial(self, source):
        with source.addParallelTask(2) as (response, request):
            with response.addRaceTask(3) as (response_ok, response_fail, response_skip):
                response_ok.addListener(Notificator.onAdvertHidden)
                response_fail.addListener(Notificator.onAdvertDisplayFailed)
            request.addFunction(AdvertisementProvider.showAdvert, "Interstitial", self.AdUnitName)
