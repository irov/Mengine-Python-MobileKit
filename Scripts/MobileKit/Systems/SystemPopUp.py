from Foundation.System import System
from Foundation.DemonManager import DemonManager
from Foundation.TaskManager import TaskManager
from MobileKit.PopUpManager import PopUpManager


class SystemPopUp(System):
    def __init__(self):
        super(SystemPopUp, self).__init__()

    def _onRun(self):
        self.addObservers()
        return True

    # observers
    def addObservers(self):
        self.addObserver(Notificator.onPopUpOpen, self._cbPopUpOpen)
        self.addObserver(Notificator.onPopUpClose, self._cbPopUpClose)
        self.addObserver(Notificator.onSceneActivate, self._cbSceneActivate)

    def _cbPopUpOpen(self, popup_id):
        if PopUpManager.hasPopUpContent(popup_id) is False:
            Trace.log("Manager", 0, "{!r} doesnt exist in PopUpManager".format(popup_id))
            return False

        PopUp = DemonManager.getDemon("PopUp")
        open_pop_ups = PopUp.getParam("OpenPopUps")

        if popup_id not in open_pop_ups:
            PopUp.appendParam("OpenPopUps", popup_id)

        self._openPopUp(PopUp)

        return False

    def _cbPopUpClose(self, popup_id):
        PopUp = DemonManager.getDemon("PopUp")
        open_pop_ups = PopUp.getParam("OpenPopUps")

        if popup_id in open_pop_ups:
            PopUp.delParam("OpenPopUps", popup_id)

        self._closePopUp(open_pop_ups)

        if PopUp.isActive() is False or PopUp.isEntityActivate() is False:
            # not in scene groups or entity is not active (or scene is None at this moment)
            return False

        return False

    def _openPopUp(self, PopUp):
        if PopUp.isEntityActivate() is False:
            task_chain = TaskManager.createTaskChain()
            with task_chain as tc:
                tc.addTask('TaskSceneLayerGroupEnable', LayerName="PopUp", Value=True)
                tc.addTask("TaskFadeIn", GroupName="FadeUI", To=0.5, Time=250.0)

    def _closePopUp(self, open_pop_ups):
        if len(open_pop_ups) == 0:
            task_chain = TaskManager.createTaskChain()
            with task_chain as tc:
                tc.addTask('TaskSceneLayerGroupEnable', LayerName="PopUp", Value=False)
                tc.addTask("TaskFadeOut", GroupName="FadeUI", To=0.5, Time=250.0)

    def _cbSceneActivate(self, scene_name):
        PopUp = DemonManager.getDemon("PopUp")
        open_pop_ups = PopUp.getParam("OpenPopUps")
        if len(open_pop_ups) != 0:
            self._openPopUp(PopUp)

        return False





