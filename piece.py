import pyglet

class Piece:
    # the #-symbol makes a blokkade
    def __init__(self, type, steps):
        self.type = type
        self.label = pyglet.text.Label(type,
                          font_name='Arial',
                          font_size=16,
                          x=self._x, y=self._y,
                          anchor_x='center', anchor_y='center')
        self.owner = 0
        self.steps = steps