import pyglet

class Piece(object):
    # the #-symbol makes a blokkade
    def __init__(self, typePiece, steps):
        self.type = typePiece
        self.size = 20
        self.owner = None
        self.hidden = False
        self.steps = steps
        self.field = None