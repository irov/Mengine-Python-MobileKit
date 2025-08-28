from Foundation.Entity.BaseEntity import BaseEntity

MOVIE_CONTENT_NAME = "Movie2_Content"


class Header(BaseEntity):

    """ Parent class for own Header """

    def __init__(self):
        super(Header, self).__init__()
        self.movie_content = None
        self.content = {}

    def _onPreparation(self):
        if self.object.hasObject(MOVIE_CONTENT_NAME) is False:
            Trace.log("Entity", 0, "{!r} not found in Header".format(MOVIE_CONTENT_NAME))
            return
        self.movie_content = self.object.getObject(MOVIE_CONTENT_NAME)

        self.setup()
        self.adjustSlotsPositions()

    def _onActivate(self):
        for elem in self.content.values():
            elem.onActivate()

    def _onDeactivate(self):
        self.movie_content = None

        for elem in self.content.values():
            elem.onFinalize()
        self.content = {}

    def _attachTo(self, movie, slot_name):
        slot = self.movie_content.getMovieSlot(slot_name)
        slot.addChild(movie.getEntityNode())

    def setupPrototype(self, object_name, prototype_name, slot_name=None, **params):
        if self.object.hasPrototype(prototype_name) is False:
            Trace.log("Entity", 0, "Prototype {!r} not found in {!r}".format(prototype_name, self.object.getName()))
            return None
        if slot_name is not None and self.movie_content.hasSlot(slot_name) is False:
            Trace.log("Entity", 0, "{!r} not found slot {!r}".format(self.movie_content.getName(), slot_name))
            return None

        movie = self.object.generateObjectUnique(object_name, prototype_name, **params)
        if slot_name is not None:
            self._attachTo(movie, slot_name)
        return movie

    def setupObject(self, movie_name, slot_name):
        if self.object.hasObject(movie_name) is False:
            Trace.log("Entity", 0, "Movie {!r} not found in {!r}".format(movie_name, self.object.getName()))
            return None
        if self.movie_content.hasSlot(slot_name) is False:
            Trace.log("Entity", 0, "{!r} not found slot {!r}".format(self.movie_content.getName(), slot_name))
            return None

        movie = self.object.getObject(movie_name)
        self._attachTo(movie, slot_name)
        return movie

    def adjustSlotsPositions(self):
        self._adjustSlotsPositions()

    def _adjustSlotsPositions(self):
        return

    def setup(self):
        self._setup()

    def _setup(self):
        return

