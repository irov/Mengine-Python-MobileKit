from Foundation.DatabaseManager import DatabaseManager
from Foundation.ObjectManager import ObjectManager


class IconManager(object):
    s_db_module = "Database"
    s_icons_db_name = "Icons"

    @staticmethod
    def generateObjectFromPrototypeORM(prototypeORM):
        object = ObjectManager.createObjectUnique(
            prototypeORM.Type,
            prototypeORM.Name,
            None,
            **prototypeORM.Params
        )
        return object

    @staticmethod
    def generateIcon(name, size=None):
        icon_db = DatabaseManager.getDatabase(
            IconManager.s_db_module,
            IconManager.s_icons_db_name
        )

        if icon_db is None:  # error handled in DatabaseManager
            return None

        icon_orm = DatabaseManager.findDB(icon_db, Prototype=name, Size=size)

        if icon_orm is None:
            Trace.log("Manager", 0,
                "[IconManager|generateIcon]"
                "\n ! fail to find icon orm"
                "\n > Module='{}' ORM='{}'"
                "\n > Name = '{}' Size = '{}'"
                .format(
                    IconManager.s_db_module, IconManager.s_icons_db_name,
                    name, size
                ))
            return None

        icon = IconManager.generateObjectFromPrototypeORM(icon_orm)

        if icon is None:
            Trace.log("Manager", 0,
                "[IconManager|generateIcon]"
                "\n ! fail to generate icon"
                "\n > Module='{}' ORM='{}'"
                "\n > Name = '{}' Size = '{}'"
                .format(
                    IconManager.s_db_module, IconManager.s_icons_db_name,
                    name, size
                ))
            return None

        return icon

    @staticmethod
    def generateIconOnNode(node, name, size=None):
        if node is None:
            Trace.log("Manager", 0,
                "[IconManager|generateIconOnNode]"
                "\n > node is None")
            return None

        icon = IconManager.generateIcon(name, size)

        if icon is None:  # error handled in generateIcon func
            return None

        icon_entity_node = icon.getEntityNode()
        node.addChild(icon_entity_node)

        return icon

    @staticmethod
    def generateIconStackOnNode(node, names, sizes, slot_name):
        icons = []

        outer_node = node
        for name, size in zip(names, sizes):
            icon = IconManager.generateIcon(name, size)

            if icon is None:
                continue

            icons.append(icon)

            icon_entity_node = icon.getEntityNode()
            outer_node.addChild(icon_entity_node)

            if icon.hasSlot(slot_name):
                outer_node = icon.getMovieSlot(slot_name)
            else:
                outer_node = icon_entity_node

        icon_stack = IconStack(icons)

        return icon_stack


class IconInterface(object):
    def setEnable(self, value):
        self._setEnable(value)

    def _setEnable(self, value):
        pass

    def onDestroy(self):
        self._onDestroy()

    def _onDestroy(self):
        pass

    def setTextAliasEnvironment(self, text_env):
        self._setTextAliasEnvironment(text_env)

    def _setTextAliasEnvironment(self, text_env):
        pass

    def getEntityNode(self):
        return self._getEntityNode()

    def _getEntityNode(self):
        return None

    def getEntity(self):
        return self._getEntity()

    def _getEntity(self):
        pass


class IconStack(IconInterface):
    def __init__(self, icons):
        self.icons = icons

    def _setEnable(self, value):
        for icon in self.icons:
            icon.setEnable(value)

    def _onDestroy(self):
        for icon in reversed(self.icons):
            node = icon.getEntityNode()
            node.removeFromParent()
            icon.onDestroy()
        self.icons = []

    def _setTextAliasEnvironment(self, text_env):
        for icon in self.icons:
            icon.setTextAliasEnvironment(text_env)

    def _getEntityNode(self):
        if not self.icons:
            return None
        return self.icons[0].getEntityNode()

    def _getEntity(self):
        if not self.icons:
            return None
        return self.icons[0].getEntity()
