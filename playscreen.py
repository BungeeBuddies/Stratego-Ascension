#Priorities: then get AIvAI to work awesome and last of all PvAI

import pyglet
import copy
from pyglet.gl import *
from field import Field
from piece import Piece
from utils import Utils
from time import sleep
import threading
from threading import Lock

class PlayScreen:

    def __init__(self, window, player1, player2):
        self.init = False
        self.window = window
        self.width = 900
        self.height = 700
        self.xOffset = self.width/4
        self.yOffset = self.height/8 + 35
        self.fieldOffset = 1
        self.barrierFields = [[2, 4], [3, 4], [6, 4], [7, 4], [2, 5], [3, 5], [6, 5], [7, 5]]

        self.player1 = player1
        self.player2 = player2
        self.currentPlayer = None

        self.widthOfField = 10
        self.heightOfField = 10
        self.sizeOfField = 25
        self.isFieldSelected = False
        self.selectedField = 0
        self.color = [1, 1, 1]

        self.aiDelay = .5

        self.visibleEnemyField = None
        self.lockdownTimer = None
        self.lockdownTime = 0.5
        self.lockdown = False
        # self.firstSelectedXPosition = None
        # self.firstSelectedYPosition = None
        self.playFields = self._createPlayField()
        self.fields = [item for sublist in self.playFields for item in sublist]

        self.selectedField = None
        self.firstSelected = None
        self._changePlayerTurnArray = [self._changePlayerTurnPvP,self._changePlayerTurnPvAI,self._changePlayerTurnAIvAI]
        self._changePlayerTurn = self._changePlayerTurnArray[2]
        self.header = pyglet.text.Label('',
                          font_name='Arial',
                          font_size=16,
                          x=self.width/2, y=self.height-20,
                          anchor_x='center', anchor_y='center')
        

        
    def handleClick(self, field):
        #if the currentPlayer is a computer, ignore all of this. Also ignore if lockdown is true
        if self.currentPlayer.isComputer or self.lockdown:
            return
        #Firstclick: check if no piece has been selected before and if there is a piece there, and if this piece is his. If all of this is true, then check if he clicked a piece which can move.
        if self.firstSelected is None and field.piece is not None:
            if field.piece.steps > 0 and field.piece.owner == self.currentPlayer:
                self.firstSelected = field
        elif self.firstSelected is not None: 
            if field is self.firstSelected:
                self.firstSelected = None
               
            elif (Utils.isLegalMove(self.firstSelected, field, self.playFields)): #if the move is legal, execute it
                self.executeMove(self.firstSelected, field)
                            


    def _onLockDownFinish(self, source, target):
        #execute the attack
        if target.piece.type is 10:
            if source.piece.type is 1:
                target.piece = source.piece
                source.piece = None
            else:
                source.piece = None
        elif target.piece.type is 'B':
            if source.piece.type is 3:
                target.piece = source.piece
                source.piece = None
            else :
                source.piece = None
        elif target.piece.type is 'F':
            self.win(self.currentPlayer)            
        else:
            if target.piece.type < source.piece.type:
                target.piece = source.piece
                source.piece = None
            elif target.piece.type is source.piece.type:
                source.piece = None
                target.piece = None
            else:
                source.piece = None
        self._changePlayerTurn()
        self.lockdown = False   

    def _changePlayerTurnPvP(self):
        if self.currentPlayer is None:
            self.currentPlayer = self.player1
            self.header.text = self.currentPlayer.name
            lastPlayer = self.player2
            for y in  self.player2.pieces:
                for piece in y:
                    if piece is not None:
                        piece.hidden = True
            return
        self.firstSelected = None
        self.visibleEnemyField = None
        lastPlayer = None
        for y in  self.currentPlayer.pieces:
            for piece in y:
                    piece.hidden = True
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
            self.lastPlayer = self.player1
        
        else:
            self.currentPlayer = self.player1
            self.lastPlayer = self.player2
        self.header.text = self.currentPlayer.name
        self.lastPlayer.isPlaying = False
        for y in  self.currentPlayer.pieces:
            for piece in y:
                    piece.hidden = False

    def _changePlayerTurnPvAI(self):
        if self.currentPlayer is None:
            self.currentPlayer = self.player1
            self.header.text = self.currentPlayer.name
            lastPlayer = self.player2
            for y in  self.player2.pieces:
                for piece in y:
                    if piece is not None:
                        piece.hidden = True
            return        
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
            self.lastPlayer = self.player1
        
        else:
            self.currentPlayer = self.player1
            self.lastPlayer = self.player2
        self.header.text = self.currentPlayer.name
        self.lastPlayer.isPlaying = False

    def _changePlayerTurnAIvAI(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
            self.lastPlayer = self.player1
        
        else:
            self.currentPlayer = self.player1
            self.lastPlayer = self.player2
        self.header.text = self.currentPlayer.name
        self.lastPlayer.isPlaying = False

    def _createPlayField(self):
        playFields = [[Field(0, 0, self.sizeOfField) for x in xrange(self.widthOfField)] for y in xrange(self.heightOfField)]

        for y in range(len(playFields)):
            for x in range(len(playFields[0])):
                playFields[y][x].x = x * playFields[y][x].size*2 + self.xOffset + self.fieldOffset * x
                playFields[y][x].y = y * playFields[y][x].size*2 + self.yOffset + self.fieldOffset * y
                if (y in range(4)):
                    playFields[y][x].piece = self.player1.pieces[y][x]
                if (y in range(6, 10)):
                    playFields[y][x].piece = self.player2.pieces[len(self.player2.pieces)-y+5][len(self.player2.pieces[-y+5])-1-x]
                try:
                    self.barrierFields.index([x, y])
                except ValueError:
                    pass
                else:
                    playFields[y][x].barrier = True
                    playFields[y][x].piece = Piece('#', 0)

        return playFields

    def draw(self):
        if self.currentPlayer is None:
            self._changePlayerTurn()
        if self.currentPlayer.isComputer and not self.currentPlayer.isPlaying:
            self.currentPlayer.play(self)
        self.header.draw()
        for y in range(0, len(self.playFields)):
            for x in range(0, len(self.playFields[y])):
                field = self.playFields[y][x]
                if (field.barrier):
                    glColor3f(1, 0, 0)
                elif (self.firstSelected is field):
                    glColor3f(1, 0, 1)
                elif (field.piece is not None):
                    if (field.piece.owner is self.player1):
                        glColor3f(1, 1, 0)
                    elif (field.piece.owner is self.player2):
                        glColor3f(0, 1, 0)
                else: 
                    glColor3f(1, 1, 1)                
                Utils.drawField(field)

    #returns true after making the move, if this fails for some reason it returns false
    def executeMove(self,source, target):
        #check if its a legal move
        if not Utils.isLegalMove(source, target, self.playFields) or self.lockdown:
            return False
        #If the target is an empty field, do it instantly
        if target.piece is None:
            target.piece = source.piece
            source.piece = None
            #If its an AI, delay the game for a bit
            if self.currentPlayer.isComputer:
                self.AIDelayTimer = threading.Timer(self.aiDelay,self._changePlayerTurn)
                self.AIDelayTimer.start()
            else:
                self._changePlayerTurn()
        #else set the timer
        else:
            print "Vechteee!"
            target.piece.hidden = False
            self.firstSelected = None
            self.lockdown = True
            self.lockdownTimer = threading.Timer(self.lockdownTime, self._onLockDownFinish,[source,target])
            self.lockdownTimer.start()
            self.lockdownTimer.join()
        return True

    def win(self,player):
        pass