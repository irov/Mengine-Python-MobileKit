from Foundation.DemonManager import DemonManager


class AdjustableScreenUtils(object):

    @staticmethod
    def getGameWidth():
        viewport = Mengine.getGameViewport()
        width = viewport.end.x - viewport.begin.x
        return width

    @staticmethod
    def getGameHeight():
        viewport = Mengine.getGameViewport()
        height = viewport.end.y - viewport.begin.y
        return height

    @staticmethod
    def getPhoneAdaptiveBannerHeight(width):
        """ Applovin Banners are automatically sized to 320x50 on phones """
        height = 50.0 * width / 320.0
        return height

    @staticmethod
    def getTabletAdaptiveBannerHeight(width):
        """ Applovin Banners are automatically sized to 728x90 on tablets """
        height = 90.0 * width / 728.0
        return height

    @staticmethod
    def getHeaderHeight():
        header = DemonManager.getDemon("Header")
        if header is None or header.isActive() is False:
            return 0.0
        return header.getHeight()

    @staticmethod
    def getMainSizes():
        """ :returns: game_width, game_height, header_height, banner_height """
        game_width = AdjustableScreenUtils.getGameWidth()
        game_height = AdjustableScreenUtils.getGameHeight()
        header_height = AdjustableScreenUtils.getHeaderHeight()
        if Mengine.hasOption("ignorebanner") is True:
            banner_height = 0.0
        else:
            banner_height = AdjustableScreenUtils.getPhoneAdaptiveBannerHeight(game_width)
        return game_width, game_height, header_height, banner_height

    @staticmethod
    def getMainSizesExt():
        """ :returns: game_width, game_height, header_height, banner_height, viewport, x_center, y_center """
        game_width, game_height, top_offset, bottom_offset = AdjustableScreenUtils.getMainSizes()
        viewport = Mengine.getGameViewport()
        x_center = viewport.begin.x + game_width / 2
        y_center = viewport.begin.y + game_height / 2
        return game_width, game_height, top_offset, bottom_offset, viewport, x_center, y_center
