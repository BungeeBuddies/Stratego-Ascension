from piece import Piece
import pyglet

class Player(object):

    def __init__(self, isComputer, pieces):
        self.isComputer = isComputer
        self.sizeOfField = 25
        self.heightOfField = 4
        self.widthOfField = 10

        self._pieces = [[None for x in xrange(self.widthOfField)] for y in xrange(self.heightOfField)]

        for y in range(len(self._pieces)):
            for x in range(len(self._pieces[y])):
                self._pieces[y][x] = pieces[y*self.widthOfField+x]

    def play(self, p2Pieces):
    	pass

    def pieces():
        doc = "The pieces property."
        def fget(self):
            return self._pieces
        def fset(self, value):
            self._pieces = value
        def fdel(self):
            del self._pieces
        return locals()
    pieces = property(**pieces())