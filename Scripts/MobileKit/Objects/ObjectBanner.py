from Foundation.Object.DemonObject import DemonObject


class ObjectBanner(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.declareParam("Show", True)

    def _onParams(self, params):
        super(ObjectBanner, self)._onParams(params)
        self.initParam("Show", params, True)
