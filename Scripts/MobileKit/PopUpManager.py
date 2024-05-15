class PopUpManager(object):

    s_contents = {}

    @staticmethod
    def importPopUpContents(module, names):
        for name in names:
            if PopUpManager.importPopUpContent(module, name) is False:
                return False
        return True

    @staticmethod
    def importPopUpContent(module, name):
        popup_content_type = Utils.importType(module, name)
        if popup_content_type is None:
            return False
        PopUpManager.addPopUpContent(popup_content_type)
        return True

    @staticmethod
    def addPopUpContent(popup_content_type):
        popup_content = popup_content_type()
        PopUpManager.s_contents[popup_content.popup_id] = popup_content

    @staticmethod
    def getPopUpContent(popup_id):
        return PopUpManager.s_contents.get(popup_id)

    @staticmethod
    def hasPopUpContent(popup_id):
        return popup_id in PopUpManager.s_contents

    @staticmethod
    def getAllPopUpContents():
        return PopUpManager.s_contents

    @staticmethod
    def onFinalize():
        for popup_content in PopUpManager.s_contents.values():
            if popup_content.isInitialized() is True:
                popup_content.onFinalize()
        PopUpManager.s_contents = {}








