from Foundation.Object.DemonObject import DemonObject


class ObjectHeader(DemonObject):

    def getHeight(self):
        if self.isActive() is False:
            Trace.log("Object", 0, "Header entity is not active!")
            return 0.0
        content = self.getObject("Movie2_Content")
        bbox = content.getCompositionBounds()
        height = bbox.maximum.y - bbox.minimum.y
        return height

    def getComponentByName(self, name):
        if self.isActive() is False:
            Trace.log("Object", 0, "Header entity is not active!")
            return None
        return self.entity.content.get(name)

    def getComponentByType(self, name):
        if self.isActive() is False:
            Trace.log("Object", 0, "Header entity is not active!")
            return None
        for component in self.entity.content.values():
            if component.__class__.__name__ == name:
                return component
        return None
