from Foundation.Object.DemonObject import DemonObject
from Foundation.SystemManager import SystemManager
from Foundation.Providers.AdPointProvider import AdPointProvider


class ObjectAdvertisingScene(DemonObject):
    ad_points_queue = []
    base_scene_name = "Advertising"

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.declareParam("NextScene")
        Type.declareParam("CacheNoAds")
        Type.declareParam("Mode")
        Type.declareParam("AdUnitName")
        Type.declareParam("AdPointName")

    def _onParams(self, params):
        super(ObjectAdvertisingScene, self)._onParams(params)
        self.initParam("NextScene", params, None)
        self.initParam("CacheNoAds", params, False)
        self.initParam("Mode", params, "Interstitial")
        self.initParam("AdUnitName", params, None)
        self.initParam("AdPointName", params, None)

    def isInterstitialEnabled(self):
        if self.getParam("CacheNoAds") is True:
            return False

        if Mengine.getConfigBool("Advertising", "Interstitial", False) is False:
            return False
        if Mengine.hasTouchpad() is False:
            if _DEVELOPMENT is True:
                Trace.msg_err("Advertising works only with touchpad! (add -touchpad)")
            return False

        SystemAdvertising = SystemManager.getSystem("SystemAdvertising")

        if SystemAdvertising.isDisabledForever() is True:
            self.setParam("CacheNoAds", True)
            return False

        return True

    def skipInterstitial(self):
        Notification.notify(Notificator.onChangeScene, self.getParam("NextScene"))

    def tryStartInterstitial(self):
        """ returns True if ad will be shown
            do not forget to put all object params before call this method!
        """
        if self._tryStartInterstitial() is False:
            self.skipInterstitial()
            return False

        Notification.notify(Notificator.onChangeScene, self.base_scene_name)
        return True

    def _checkAdPoint(self, ad_point_name):
        """ checks if interstitial is allowed and ad point exists, enabled """
        if self.isInterstitialEnabled() is False:
            return False

        if ad_point_name is None:
            Trace.log("Object", 0, "AdPointName not found")
            return False

        if AdPointProvider.hasAdPoint(ad_point_name) is False:
            Trace.log("Object", 0, "AdPoint {!r} not found".format(ad_point_name))
            return False

        if AdPointProvider.isEnabledAdPoint(ad_point_name) is False:
            return False

        return True

    def _tryStartInterstitial(self):
        """ trigger and check ad point if ready to show ad """
        ad_point_name = self.getParam("AdPointName")

        if self._checkAdPoint(ad_point_name) is False:
            return False

        ad_point_params = AdPointProvider.getAdPointParams(ad_point_name)
        AdPointProvider.triggerAdPoint(ad_point_name)
        if AdPointProvider.checkAdPoint(ad_point_name) is False:
            return False

        self.setParams(AdUnitName=ad_point_params.ad_unit_name, Mode=ad_point_params.ad_type)
        return True

    def addQueueAdPoint(self, ad_point_name):
        if self._checkAdPoint(ad_point_name) is False:
            return False

        self.ad_points_queue.append(ad_point_name)
        return True

    def startQueueAdPoints(self, next_scene):
        self.setParam("NextScene", next_scene)

        ready_ad_points = []
        for ad_point_name in self.ad_points_queue:
            AdPointProvider.triggerAdPoint(ad_point_name)
            if AdPointProvider.checkAdPoint(ad_point_name) is True:
                ready_ad_points.append(ad_point_name)

        self.ad_points_queue = ready_ad_points

        if len(self.ad_points_queue) > 0:
            Notification.notify(Notificator.onChangeScene, self.base_scene_name)
        else:
            self.skipInterstitial()

