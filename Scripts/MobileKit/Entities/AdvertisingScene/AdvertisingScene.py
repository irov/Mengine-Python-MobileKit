from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.Providers.AdPointProvider import AdPointProvider
from Foundation.Providers.AdvertisementProvider import AdvertisementProvider


class AdvertisingScene(BaseEntity):

    """ How To:

    > from Foundation.DemonManager import DemonManager
    > AdvertisingScene = DemonManager.getDemon("AdvertisingScene")

    CASE 1: just try to show interstitial or Rewarded

        > AdvertisingScene.setParams(Mode="Interstitial", AdUnitName="TestAdUnit", NextScene="Lobby")
        > AdvertisingScene.tryStartInterstitial()

    CASE 2: try to start AdPoint (trigger ad point, check if ad point is ready, do transition)

        > AdvertisingScene.setParams(AdPointName="ad_interstitial_level_start", NextScene="GameArea")
        > AdvertisingScene.tryStartInterstitial()

    CASE 3: try to start few ad points in a row

        > AdvertisingScene.addQueueAdPoint("ad_interstitial_level_lose")
        > AdvertisingScene.addQueueAdPoint("ad_interstitial_level_end")
        > # checks all ad points (trigger, check ready), show ad (if possible)
        > AdvertisingScene.startQueueAdPoints("GameOver")
    """

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
        Type.addAction(Type, "AdPointName")

    def _onPreparation(self):
        if _DEVELOPMENT is True and self.object.hasObject("Movie2_Content"):
            movie = self.object.getObject("Movie2_Content")
            movie.setEnable(True)

    def _onActivate(self):
        self.__runTaskChain()

    def _onDeactivate(self):
        if self.tc is not None:
            self.tc.cancel()
            self.tc = None

    def __runTaskChain(self):
        if self.tc is not None:
            self.tc.cancel()
        self.tc = TaskManager.createTaskChain()

        with self.tc as tc:
            tc.addScope(self._scopeMain)
            tc.addDelay(1)  # necessary for transition
            with tc.addIfTask(lambda: len(self.object.ad_points_queue) == 0) as (if_empty, if_not_empty):
                if_empty.addNotify(Notificator.onChangeScene, self.NextScene)
                if_not_empty.addFunction(self.__runTaskChain)

    def _scopeMain(self, source):
        if len(self.object.ad_points_queue) != 0:
            ad_point_params = AdPointProvider.getAdPointParams(self.object.ad_points_queue.pop(0))
            self.object.setParam("Mode", ad_point_params.ad_type)
            self.object.setParam("AdUnitName", ad_point_params.ad_unit_name)
            self.object.setParam("AdPointName", ad_point_params.name)

        if self.AdPointName is not None:
            source.addScope(self._scopeAdPoint)
        elif self.Mode == "Interstitial":
            source.addScope(self._scopeInterstitial)
        elif self.Mode == "Rewarded":
            source.addScope(self._scopeRewarded)
        else:
            Trace.log("Entity", 0, "AdvertisingScene: Unknown Mode: {}".format(self.Mode))

        source.addFunction(self.object.setParam, "AdUnitName", None)
        source.addFunction(self.object.setParam, "AdPointName", None)
        source.addFunction(self.object.setParam, "Mode", None)

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

    def _scopeAdPoint(self, source):
        with source.addParallelTask(2) as (response, request):
            # react on advert
            with response.addRaceTask(2) as (hidden, fail):
                hidden.addListener(Notificator.onAdvertHidden)
                fail.addListener(Notificator.onAdvertDisplayFailed)

            # reset counter and show advert
            request.addFunction(AdPointProvider.startAdPoint, self.AdPointName)

