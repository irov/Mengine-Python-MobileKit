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

        movie = PrototypeManager._generateObjectUnique(params_orm.Prototype, object_name)
        if movie is None:
            return None

        icon = None
        param_prototype = params_orm.Icon.get("Prototype")
        param_size = params_orm.Icon.get("Size")
        param_slot = params_orm.Icon.get("Slot")

        if param_prototype is not None:
            icon = IconManager.generateIcon(param_prototype, param_size)

            if params_orm.Type == "Movie2Button":
                movie.addChildToSlot(icon.getEntityNode(), param_slot)
            else:
                slot = movie.getMovieSlot(param_slot)
                slot.addChild(icon.getEntityNode())

        container = ObjectContainer(movie, icon)

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

    def getEntityNode(self):
        return self.movie.getEntityNode()

    def getCompositionBounds(self):
        return self.movie.getCompositionBounds()

    def setParam(self, key, value):
        self.movie.setParam(key, value)
        if self.icon is not None:
            self.icon.setParam(key, value)
