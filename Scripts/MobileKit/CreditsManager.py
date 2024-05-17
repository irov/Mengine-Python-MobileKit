from Foundation.DatabaseManager import DatabaseManager
from Foundation.Manager import Manager


class CreditsManager(Manager):
    s_params = []

    @staticmethod
    def loadParams(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)
        for record in records:
            group_name = str(record.get("GroupName"))
            prototype = str(record.get("Movie2Prototype"))
            offset = float(record.get("OffsetTop"))
            alias_id = str(record.get("AliasId"))
            text_id = str(record.get("TextId"))
            slot = str(record.get("Slot"))

            param = CreditsParam(group_name, prototype, offset, alias_id, text_id, slot)
            CreditsManager.s_params.append(param)

        return True

    @staticmethod
    def getParams():
        if len(CreditsManager.s_params) == 0:
            Trace.log("Manager", 0, "Languages params is empty!")

        return CreditsManager.s_params


class CreditsParam(object):
    def __init__(self, group_name, prototype, offset, alias_id, text_id, slot):
        self.group_name = group_name
        self.prototype = prototype
        self.offset = offset
        self.alias_id = alias_id
        self.text_id = text_id
        self.slot = slot

    def get(self):
        return self.group_name, self.prototype, self.offset, self.alias_id, self.text_id, self.slot
