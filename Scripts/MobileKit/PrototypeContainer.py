class PrototypeContainer(object):
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

    def getLayoutSize(self):
        size = self.getSize()
        return (size.x, size.y)

    def setLayoutOffset(self, layout_box, layout_offset, layout_size):
        layout_box_width, layout_box_height = layout_box.getSize()
        self.setLocalPosition((
            layout_offset[0] + layout_size[0]/2 - layout_box_width/2,
            layout_offset[1] + layout_size[1]/2 - layout_box_height/2
        ))