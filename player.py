from piece import Piece
from time import sleep
from utils import Utils
import random
import pyglet

class Player(object):

    def __init__(self, isComputer, pieces,name):
        self.isComputer = isComputer
        self.sizeOfField = 25
        self.heightOfField = 4
        self.widthOfField = 10
        self.name = name
        self._pieces = [[None for x in xrange(self.widthOfField)] for y in xrange(self.heightOfField)]
        self.isPlaying = False
        

        for y in range(len(self._pieces)):
            for x in range(len(self._pieces[y])):
                self._pieces[y][x] = pieces[y*self.widthOfField+x]
                self._pieces[y][x].owner = self

    def play(self, playScreen):
        self.isPlaying = True
        fields = playScreen.playFields
        playableMoves = {}

        for row in self._pieces:
            for piece in row:
                if piece is not None:
                    step = piece.steps+1
                    index = Utils.getFieldIndex(piece, fields)
                    if index is not None: #Piece has died, apparently
                        y = index[0]
                        x = index[1]

                        # Up
                        for up in range(y, y+step if y+step <= len(fields) else len(fields)):
                            if Utils.isLegalMove(fields[y][x], fields[up][x], fields):
                                if fields[up][x].piece is None or fields[up][x].piece is not None and fields[up][x].piece.owner is not piece.owner:
                                    playableMoves[fields[y][x]] = fields[up][x]

                        # Down
                        for down in range(y-step if y-step > 0 else 0, y):
                            if Utils.isLegalMove(fields[y][x], fields[down][x], fields):
                                if fields[down][x].piece is None or fields[down][x].piece is not None and fields[down][x].piece.owner is not piece.owner:
                                    playableMoves[fields[y][x]] = fields[down][x]
                        
                        # Right
                        for right in range(x, x+step if x+step <= len(fields) else len(fields)):
                            if Utils.isLegalMove(fields[y][x], fields[y][right], fields):
                                if fields[y][right].piece is None or fields[y][right].piece is not None and fields[y][right].piece.owner is not piece.owner:
                                    playableMoves[fields[y][x]] = fields[y][right]
                        
                        # Left
                        for left in range(x-step if x-step > 0 else 0, x):
                            if Utils.isLegalMove(fields[y][x], fields[y][left], fields):
                                if fields[y][left].piece is None or fields[y][left].piece is not None and fields[y][left].piece.owner is not piece.owner:
                                    playableMoves[fields[y][x]] = fields[y][left]
        if (len(playableMoves) > 0):
            move = random.choice(playableMoves.keys())
            sourceField = move
            targetField = playableMoves[move]
            playScreen.executeMove(sourceField, targetField)
            return

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