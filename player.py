from piece import Piece
from time import sleep
from utils import Utils
import random
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
                self._pieces[y][x].owner = self

    def play(self, fields):

        playablePieces = {}

        for row in self._pieces:
            for piece in row:
                step = piece.steps+1
                index = Utils.getFieldIndex(piece.field, fields)
                y = index[0]
                x = index[1]

                # Up
                for up in range(y, y+step if y+step <= len(fields) else len(fields)):
                    if fields[up][x].piece is None and Utils.isLegalMove(piece.field, fields[up][x], fields):
                        playablePieces[piece.field] = fields[up][x]

                # Down
                for down in range(y-step if y-step > 0 else 0, y):
                    if fields[down][x].piece is None and Utils.isLegalMove(piece.field, fields[down][x], fields):
                        playablePieces[piece.field] = fields[down][x]
                
                # Right
                for right in range(x, x+step if x+step <= len(fields) else len(fields)):
                    if fields[y][right].piece is None and Utils.isLegalMove(piece.field, fields[y][right], fields):
                        playablePieces[piece.field] = fields[y][right]
                
                # Left
                for left in range(x-step if x-step > 0 else 0, x):
                    if fields[y][left].piece is None and Utils.isLegalMove(piece.field, fields[y][left], fields):
                        playablePieces[piece.field] = fields[y][left]

        if (len(playablePieces) > 0):
            move = random.choice(playablePieces.keys())

            tempPiece = playablePieces[move].piece
            tempField = playablePieces[move]

            # Target
            playablePieces[move].piece = move.piece
            playablePieces[move] = move
            
            # Source
            move.piece = tempPiece
            move = tempField
            

        return True

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