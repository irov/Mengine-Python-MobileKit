from Foundation.DatabaseManager import DatabaseManager
from Foundation.Manager import Manager
from Foundation.GroupManager import GroupManager


class CreditsManager(Manager):
    s_orms = []

    @staticmethod
    def loadParams(module, param):
        orms = DatabaseManager.getDatabaseORMs("Database", "Credits")

        for orm in orms:
            if GroupManager.hasPrototype(orm.GroupName, orm.Movie2Prototype):
                CreditsManager.s_orms.append(orm)

        return True
        pass

    @staticmethod
    def getParams():
        if len(CreditsManager.s_orms) == 0:
            Trace.log("Manager", 0, "Languages params is empty!")

        return CreditsManager.s_orms

