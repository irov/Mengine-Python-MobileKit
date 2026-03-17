def onInitialize():
    Trace.msg_dev("MobileKit onInitialize")

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

    EntityTypes = [
        {"Type": "AdvertisingScene", "Override": True}
        , "Header"
        , "Banner"
        , "PopUp"
    ]

    from Foundation.Bootstrapper import Bootstrapper

    if Bootstrapper.loadEntities("MobileKit", EntityTypes) is False:
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

    from Foundation.AdjustableScreenUtils import AdjustableScreenUtils

    Headers = [
        "Header"
    ]
    AdjustableScreenUtils.registerHeaders(Headers)

    # uncomment if you want to add new params for each account
    """
    from Foundation.AccountManager import AccountManager
    def accountSetuper(accountID, isGlobal):
        if isGlobal is True:
            return

    AccountManager.addCreateAccountExtra(accountSetuper)
    """

    return True


def onFinalize():
    Trace.msg_dev("MobileKit onFinalize")

    from MobileKit.PopUpManager import PopUpManager
    PopUpManager.onFinalize()

