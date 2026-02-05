from Foundation.Manager import Manager
from Foundation.GroupManager import GroupManager
from Foundation.DatabaseManager import DatabaseManager
from MobileKit.IconManager import IconManager
from MobileKit.PrototypeContainer import PrototypeContainer

class PrototypeManager(Manager):
    s_group = "UIStore"
    s_db_module = "Database"
    s_db_name = "Prototypes"

    @staticmethod
    def _generateObjectUnique(prototype_name, object_name, object_params):
        if _DEVELOPMENT is True and GroupManager.hasPrototype(PrototypeManager.s_group, prototype_name) is False:
            Trace.log("Manager", 0, "Not found prototype {!r} in {!r}".format(prototype_name, PrototypeManager.s_group))
            return

        movie = GroupManager.generateObjectUnique(
            object_name,
            PrototypeManager.s_group,
            prototype_name,
            **object_params if object_params is not None else {}
        )
        return movie

    @staticmethod
    def generateObjectContainerOnNode(node, name, object_name=None, object_params=None, **params):
        """ **params: Size, Color
            :returns: PrototypeContainer ( contains movie and icon (optional) )
         """
        container = PrototypeManager.generateObjectContainer(name, object_name, object_params, **params)

        if container is None:
            return None

        entity_node = container.movie.getEntityNode()
        node.addChild(entity_node)

        return container

    @staticmethod
    def generateObjectContainer(name, object_name=None, object_params=None, **params):
        """ **params: Size, Color
            :returns: PrototypeContainer ( contains movie and icon (optional) )
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

        object_unique = PrototypeManager._generateObjectUnique(params_orm.Prototype, object_name, object_params)
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

        container = PrototypeContainer(object_unique, icon)

        return container

    @staticmethod
    def generateObjectUnique(name, object_name=None, object_params=None, **params):
        """ **params: Size, Color
            :returns: Object (default)
         """
        container = PrototypeManager.generateObjectContainer(name, object_name, object_params, **params)

        if container is None:
            return None

        return container.movie

    @staticmethod
    def generateObjectUniqueOnNode(node, name, object_name=None, object_params=None, **params):
        """ **params: Size, Color
            :returns: Object (default)
         """
        container = PrototypeManager.generateObjectContainerOnNode(node, name, object_name, object_params, **params)

        if container is None:
            return None

        return container.movie
