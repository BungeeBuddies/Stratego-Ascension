from piece import Piece
import pyglet
class Field(object):

    def __init__(self, x, y, size):
        self._x = x
        self._y = y
        self.barrier = False
        self.size = size
        self.color = [1, 1, 1]
        self.selected = False
        self._piece = None
        self._label = pyglet.text.Label('',
                font_name='Arial',
                font_size=16,
                x=12, y=12,
                anchor_x='center', anchor_y='center')

    def draw():
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', 
                    (self.x + self.size, self.y + self.size, 
                    self.x - self.size, self.y + self.size)))

    def x():
        doc = "The x property."
        def fget(self):
            return self._x
        def fset(self, value):            
            self.label.x = value
            self._x = value
        def fdel(self):
            del self._x
        return locals()
    x = property(**x())

    def y():
        doc = "The y property."
        def fget(self):
            return self._y
        def fset(self, value):
            self._y = value
            self.label.y = value

        def fdel(self):
            del self._y
        return locals()
    y = property(**y())

    def piece():
        doc = "The piece property."
        def fget(self):
            return self._piece
        def fset(self, value):
            self._piece = value
            if (value is not None):
                self._piece.field = self
            # self.label.text = str(value.type)

        def fdel(self):
            del self._piece
        return locals()
    piece = property(**piece())

    def label():
        doc = "The label property."
        def fget(self):
            if self._piece is not None:
                if self._piece.hidden:
                    self._label.text = '?'
                else:
                    self._label.text = str(self._piece.type)
            return self._label
        def fset(self, value):
            self._label = value
        def fdel(self):
            del self._label
        return locals()
    label = property(**label())
