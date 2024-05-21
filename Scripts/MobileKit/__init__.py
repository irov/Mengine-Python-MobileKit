def onInitialize():
    from Foundation.Notificator import Notificator

    identities = [
        "onPopUpOpen"
        , "onPopUpClose"

    ]
    Notificator.addIdentities(identities)

    from TraceManager import TraceManager

    Traces = [
        "HeaderComponent"
        , "PopUp"
    ]
    TraceManager.addTraces(Traces)

    from Foundation.EntityManager import EntityManager
    from Foundation.ObjectManager import ObjectManager

    Types = [
        "AdvertisingScene"
        , "Header"
        , "Banner"
        , "PopUp"
    ]
    if EntityManager.importEntities("MobileKit.Entities", Types) is False:
        return False
    if ObjectManager.importObjects("MobileKit.Objects", Types) is False:
        return False

    from MobileKit.PopUpManager import PopUpManager

    PopUpContents = [
        "Credits"
        , "Settings"
        , "TechSupport"
        , "Languages"
    ]
    if PopUpManager.importPopUpContents("MobileKit.PopUpContents", PopUpContents) is False:
        return False

    # uncomment if you want to add new params for each account
    """
    from Foundation.AccountManager import AccountManager
    def accountSetuper(accountID, isGlobal):
        if isGlobal is True:
            return

    AccountManager.setCreateAccount(accountSetuper)
    """

    return True


def onFinalize():
    from MobileKit.PopUpManager import PopUpManager
    PopUpManager.onFinalize()

