from piece import Piece
from setupscreen import SetupScreen
from time import sleep
from utils import Utils
import random
from random import choice
import pyglet
import operator
from copy import copy
from pyglet.gl import *


class Player(object):

    def __init__(self, isComputer, pieces, name):
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

        self.knownPieces = []

    # def playSound(self):
    #     music = pyglet.resource.media('sounds/scifi003.mp3')
    #     musicPlayer = pyglet.media.ManagedSoundPlayer()
    #     musicPlayer.volume = 0.1
    #     musicPlayer.queue(music)
    #     musicPlayer.play()
  
    def play(self, playScreen):
        self.isPlaying = True
        fields = playScreen.playFields
        
        # Choose own move
        playableMoves = {}
        key = 0
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
                                    playableMoves[key] = moveDTO(x, y, x, up)
                                    key +=1                       
                        
                        # Right
                        for right in range(x, x+step if x+step <= len(fields) else len(fields)):
                            if Utils.isLegalMove(fields[y][x], fields[y][right], fields):
                                if fields[y][right].piece is None or fields[y][right].piece is not None and fields[y][right].piece.owner is not piece.owner:
                                    playableMoves[key] = moveDTO(x, y, right, y)
                                    key +=1
                        
                        # Left
                        for left in range(x-step if x-step > 0 else 0, x):
                            if Utils.isLegalMove(fields[y][x], fields[y][left], fields):
                                if fields[y][left].piece is None or fields[y][left].piece is not None and fields[y][left].piece.owner is not piece.owner:
                                    playableMoves[key] = moveDTO(x, y, left, y)
                                    key +=1

                        # Down
                        for down in range(y-step if y-step > 0 else 0, y):
                            if Utils.isLegalMove(fields[y][x], fields[down][x], fields):
                                if fields[down][x].piece is None or fields[down][x].piece is not None and fields[down][x].piece.owner is not piece.owner:
                                    playableMoves[key] = moveDTO(x, y, x, down)
                                    key +=1
        
        if (len(playableMoves) > 0):

            # -1 = Don't do anything
            # 0 = Random
            # 1 = Enemy in range
            # 2 = Known enemy in range
            # 3 = Weaker known enemy in range

            movesScore = {}
            for move in playableMoves.keys():
                movesScore[move] = 0

                sourceY = playableMoves[move].sourceY
                sourceX = playableMoves[move].sourceX
                targetY = playableMoves[move].targetY
                targetX = playableMoves[move].targetX

                sourcePiece = fields[sourceY][sourceX].piece
                targetPiece = fields[targetY][targetX].piece

                if targetPiece is not None:
                    movesScore[move] += 1

                    if targetPiece in self.knownPieces:
                        movesScore[move] += 1
                        
                        # If target is a bomb
                        if (targetPiece.type is 'B'):
                            if (sourcePiece.type is 3):
                                movesScore[move] = 4

                        # If target is not a bomb
                        else:
                            # If source is stronger than target, set highest priority
                            if targetPiece.type < sourcePiece.type:
                                movesScore[move] += 1

                            # If source is a spy and target is a marshall, set highest priority
                            elif sourcePiece.type is 1 and targetPiece.type is 10:
                                movesScore[move] = 5
                            
                            # Else do nothing
                            else:
                                movesScore[move] = -1

            highestScore = max(movesScore.iteritems(), key=operator.itemgetter(1))[1]
            highestMoves = []

            for score in movesScore:
                if movesScore[score] is highestScore:
                    highestMoves.append(score)

            highestMove = playableMoves[choice(highestMoves)]

            playScreen.executeMove(fields[highestMove.sourceY][highestMove.sourceX], 
                fields[highestMove.targetY][highestMove.targetX])

            attackedField = fields[highestMove.targetY][highestMove.targetX]

            if (attackedField is not None):
                self.knownPieces.append(attackedField.piece)

            # Draw movement line
            glLineWidth(5.0)
            glBegin(GL_LINES)
            glColor3f(1, 0, 1)
            glVertex2f(fields[highestMove.sourceY][highestMove.sourceX].x, fields[highestMove.sourceY][highestMove.sourceX].y)
            glVertex2f(fields[highestMove.targetY][highestMove.targetX].x, fields[highestMove.targetY][highestMove.targetX].y)
            glEnd()
            glLineWidth(1.0)

        return

    def setuppieces(self,bottomArea,topArea):
        #topArea
        self.firstSelected = None
        regels = bottomArea
        emptyfields = [f for r in regels for f in r if f.piece is not None]
        topping = topArea
        tobefilledfields = [f for r in topping for f in r if f.piece is None]
        random.shuffle(emptyfields)
        for (a, b) in zip(emptyfields, tobefilledfields):
            b.piece = a.piece
            a.piece = None

    def movementPossible(self, playScreen):
        fields = playScreen.playFields
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
                                    return True
                        
                        # Right
                        for right in range(x, x+step if x+step <= len(fields) else len(fields)):
                            if Utils.isLegalMove(fields[y][x], fields[y][right], fields):
                                if fields[y][right].piece is None or fields[y][right].piece is not None and fields[y][right].piece.owner is not piece.owner:
                                    return True
                        
                        # Left
                        for left in range(x-step if x-step > 0 else 0, x):
                            if Utils.isLegalMove(fields[y][x], fields[y][left], fields):
                                if fields[y][left].piece is None or fields[y][left].piece is not None and fields[y][left].piece.owner is not piece.owner:
                                    return True

                        # Down
                        for down in range(y-step if y-step > 0 else 0, y):
                            if Utils.isLegalMove(fields[y][x], fields[down][x], fields):
                                if fields[down][x].piece is None or fields[down][x].piece is not None and fields[down][x].piece.owner is not piece.owner:
                                    return True
        return False

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

class moveDTO:
    def __init__(self, sourceX, sourceY, targetX, targetY):
        self.sourceY = sourceY
        self.sourceX = sourceX
        self.targetX = targetX
        self.targetY = targetY