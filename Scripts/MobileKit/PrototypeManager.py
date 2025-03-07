from Foundation.GroupManager import GroupManager
from Foundation.DatabaseManager import DatabaseManager
from MobileKit.IconManager import IconManager


class PrototypeManager(object):
    s_group = "UIStore"
    s_db_module = "Database"
    s_db_name = "Prototypes"

    @staticmethod
    def _generateObjectUnique(prototype_name, object_name, **params):
        if GroupManager.hasPrototype(PrototypeManager.s_group, prototype_name) is False:
            Trace.log("Manager", 0, "Not found prototype {!r} in {!r}".format(prototype_name, PrototypeManager.s_group))
            return

        movie = GroupManager.generateObjectUnique(
            object_name,
            PrototypeManager.s_group,
            prototype_name,
            **params
        )
        return movie

    @staticmethod
    def generateObjectUniqueOnNode(node, name, object_name=None, **params):
        """ **params: Size, Color
            :returns: Object (default)
         """
        container = PrototypeManager.generateObjectContainerOnNode(node, name, object_name, **params)
        if container is not None:
            return container.movie
        return None

    @staticmethod
    def generateObjectContainerOnNode(node, name, object_name=None, **params):
        """ **params: Size, Color
            :returns: ObjectContainer ( contains movie and icon (optional) )
         """
        container = PrototypeManager.generateObjectContainer(name, object_name, **params)

        if container is None:
            return None

        entity_node = container.movie.getEntityNode()
        node.addChild(entity_node)

        return container

    @staticmethod
    def generateObjectUnique(name, object_name=None, **params):
        """ **params: Size, Color
            :returns: Object (default)
         """
        container = PrototypeManager.generateObjectContainer(name, object_name, **params)
        if container is not None:
            return container.movie
        return None

    @staticmethod
    def generateObjectContainer(name, object_name=None, **params):
        """ **params: Size, Color
            :returns: ObjectContainer ( contains movie and icon (optional) )
         """

        db = DatabaseManager.getDatabase(
            PrototypeManager.s_db_module,
            PrototypeManager.s_db_name
        )
        if db is None:
            return None

        params_orm = DatabaseManager.findDB(db, Name=name, **params)
        if params_orm is None:
            Trace.log("Manager", 0, "Not found Name={!r} in db {!r}".format(name, PrototypeManager.s_db_name))
            return None

        if object_name is None:
            object_name = params_orm.ObjectName

        object_unique = PrototypeManager._generateObjectUnique(params_orm.Prototype, object_name)
        if object_unique is None:
            return None

        icon = None
        param_prototype = params_orm.Icon.get("Prototype")
        param_size = params_orm.Icon.get("Size")
        param_slot = params_orm.Icon.get("Slot")

        if param_prototype is not None:
            icon = IconManager.generateIcon(param_prototype, param_size)
            icon_node = icon.getEntityNode()
            object_type = object_unique.getType()

            if object_type in ["ObjectMovie2Button", "ObjectMovie2CheckBox"]:
                object_unique.addChildToSlot(icon_node, param_slot)
            elif object_type in ["ObjectMovie2"]:
                slot = object_unique.getMovieSlot(param_slot)
                slot.addChild(icon_node)

        container = ObjectContainer(object_unique, icon)

        return container


class ObjectContainer(object):

    def __init__(self, movie, icon=None):
        self.movie = movie
        self.icon = icon

    def setEnable(self, state):
        self.movie.setEnable(state)
        if self.icon is not None:
            self.icon.setEnable(state)

    def onDestroy(self):
        if self.movie is not None:
            self.movie.onDestroy()
            self.movie = None
        if self.icon is not None:
            self.icon.onDestroy()
            self.icon = None

    def setTextAliasEnvironment(self, text_env):
        self.movie.setTextAliasEnvironment(text_env)
        if self.icon is not None:
            self.icon.setTextAliasEnvironment(text_env)

    def setLocalPosition(self, pos):
        node = self.movie.getEntityNode()
        node.setLocalPosition(pos)

    def getLocalPosition(self):
        node = self.movie.getEntityNode()
        return node.getLocalPosition()

    def getEntityNode(self):
        return self.movie.getEntityNode()

    def attachTo(self, node):
        root = self.movie.getEntityNode()
        root.removeFromParent()
        node.addChild(root)

    def getCompositionBounds(self):
        return self.movie.getCompositionBounds()

    def getSize(self):
        bounds = self.movie.getCompositionBounds()
        size = Utils.getBoundingBoxSize(bounds)
        return size

    def setParam(self, key, value):
        self.movie.setParam(key, value)
        if self.icon is not None:
            self.icon.setParam(key, value)
