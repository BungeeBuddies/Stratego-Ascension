import pyglet

class Piece(object):
    # the #-symbol makes a blokkade
    def __init__(self, typePiece, steps):
        self.type = typePiece
        self._field = None
        self.label = pyglet.text.Label(str(self.type),
                        font_name='Arial',
                        font_size=16,
                        x=0, y=0,
                        anchor_x='center', anchor_y='center')
        self.size = 20
        self.owner = None
        self.hidden = False
        self.steps = steps


    def field():
        doc = "The field property."
        def fget(self):
            return self._field
        def fset(self, value):
            self._field = value
            # self.label.x = self._field.x
            # self.label.y = self._field.y
        def fdel(self):
            del self._field
        return locals()
    field = property(**field())