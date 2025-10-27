from Foundation.Object.DemonObject import DemonObject


class ObjectPopUp(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)

        Type.declareParam("OpenPopUps")

    def _onParams(self, params):
        super(ObjectPopUp, self)._onParams(params)

        self.initParam('OpenPopUps', params, [])

