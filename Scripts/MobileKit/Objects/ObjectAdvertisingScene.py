from Foundation.Object.DemonObject import DemonObject
from Foundation.SystemManager import SystemManager
from Foundation.Providers.AdvertisementProvider import AdvertisementProvider


class ObjectAdvertisingScene(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addParam(Type, "NextScene")
        Type.addParam(Type, "CacheNoAds")
        Type.addParam(Type, "Mode")
        Type.addParam(Type, "AdUnitName")

    def _onParams(self, params):
        super(ObjectAdvertisingScene, self)._onParams(params)
        self.initParam("NextScene", params, None)
        self.initParam("CacheNoAds", params, False)
        self.initParam("Mode", params, "Interstitial")
        self.initParam("AdUnitName", params, None)

    def isInterstitialReady(self):
        if Mengine.hasOption("noads") is True:
            return False

        if self.getParam("CacheNoAds") is True:
            return False
        if Mengine.getConfigBool('Advertising', "Interstitial", False) is False:
            return False

        SystemAdvertising = SystemManager.getSystem("SystemAdvertising")

        if SystemAdvertising.isDisabledForever() is True:
            self.setParam("CacheNoAds", True)
            return False

        SystemAdvertising.increaseTriggerCounter()

        if SystemAdvertising.isReadyToView() is False:
            return False

        if SystemAdvertising.isInterstitialParamEnable("trigger") is True:
            # time-based ads already check availability in isReadyToView #fixme
            ad_unit_name = self.getParam("AdUnitName")
            if AdvertisementProvider.isAdvertAvailable("Interstitial", ad_unit_name) is False:
                return False

        return True

    def runNextScene(self):
        next_scene = self.getParam("NextScene")
        Notification.notify(Notificator.onChangeScene, next_scene)

    def runAdvertScene(self):
        Notification.notify(Notificator.onChangeScene, "Advertising")

