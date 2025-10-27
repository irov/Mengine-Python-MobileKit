from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.Providers.AdvertisementProvider import AdvertisementProvider


class Banner(BaseEntity):
    def __init__(self):
        super(Banner, self).__init__()

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        Type.addActionActivate("Show", Update=Banner._updateShow)

    def _updateShow(self, state):
        if state is True:
            AdvertisementProvider.showBanner(AdUnitName="Banner")
        else:
            AdvertisementProvider.hideBanner(AdUnitName="Banner")

    def _onDeactivate(self):
        # AdvertisementProvider.hideBanner(AdUnitName="Banner")
        pass
