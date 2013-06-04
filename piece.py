import pyglet

class Piece(object):
    # the #-symbol makes a blokkade
    def __init__(self, typePiece, steps):
        self.type = typePiece
        self._field = None
        self.label = None
        self.size = 20
        self.owner = 0
        self.steps = steps


    def field():
        doc = "The field property."
        def fget(self):
            return self._field
        def fset(self, value):
            self._field = value
            self.label = pyglet.text.Label(str(self.type),
                        font_name='Arial',
                        font_size=16,
                        x=self._field.x, y=self._field.y,
                        anchor_x='center', anchor_y='center')
        def fdel(self):
            del self._field
        return locals()
    field = property(**field())