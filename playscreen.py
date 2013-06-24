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

        self.aiDelay = 1.0
        self.lockdownTimer = None
        self.lockdownTime = 0.5
        self.lockdown = False

        self.playFields = self._createPlayField()
        self.fields = [item for sublist in self.playFields for item in sublist]


        self.selectedField = None
        self.firstSelected = None
        self._changePlayerTurnArray = [self._changePlayerTurnPvP, self._changePlayerTurnPvAI, self._changePlayerTurnAIvAI]
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
            if field.piece.steps > 0 and field.piece.owner is self.currentPlayer:
                self.firstSelected = field
        elif self.firstSelected is not None: 
            if field is self.firstSelected:
                self.firstSelected = None
            elif field.piece is not None and field.piece.owner is self.currentPlayer:
                pass               
            elif Utils.isLegalMove(self.firstSelected, field, self.playFields): #if the move is legal, execute it
                self.executeMove(self.firstSelected, field)

    def playSound(self):
            music = pyglet.resource.media('sounds/battle003.mp3')
            musicPlayer = pyglet.media.ManagedSoundPlayer()
            musicPlayer.queue(music)
            musicPlayer.play()

    def _onLockDownFinish(self, source, target):
        #execute the attack
        if target.piece.type is 10:
            self.playSound()
            if source.piece.type is 1:
                target.piece = source.piece
                source.piece = None
            elif source.piece.type  == target.piece.type:
                target.piece = None
                source.piece = None
            else:
                source.piece = None
        elif target.piece.type is 'B':
            self.playSound()
            if source.piece.type is 3:
                target.piece = source.piece
                source.piece = None
            else :
                source.piece = None
        elif target.piece.type is 'F':
            self.win(self.currentPlayer)            
        else:
            # self.playSound()
            if target.piece.type < source.piece.type:
                target.piece = source.piece
                source.piece = None
            elif target.piece.type == source.piece.type:
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
        if not self.currentPlayer.movementPossible(self):
            self.win(self.lastPlayer)
        for y in  self.currentPlayer.pieces:
            for piece in y:
                    piece.hidden = False

    def _changePlayerTurnPvAI(self):
        self.firstSelected = None
        lastPlayer = None   
        if self.currentPlayer is self.player1:
            self.currentPlayer = self.player2
            self.lastPlayer = self.player1
        
        else:
            self.currentPlayer = self.player1
            self.lastPlayer = self.player2
        self.header.text = self.currentPlayer.name
        self.lastPlayer.isPlaying = False
        if not self.currentPlayer.movementPossible(self):
            self.win(self.lastPlayer)
        for y in self.player2.pieces:
            for piece in y:
                if piece is not None:
                    piece.hidden = True

    def _changePlayerTurnAIvAI(self):
        self.firstSelected = None
        lastPlayer = None
        if self.currentPlayer is self.player1:
            self.currentPlayer = self.player2
            self.lastPlayer = self.player1
        
        else:
            self.currentPlayer = self.player1
            self.lastPlayer = self.player2
        if not self.currentPlayer.movementPossible(self):
            self.win(self.lastPlayer)
        self.header.text = self.currentPlayer.name
        self.lastPlayer.isPlaying = False

    def _createPlayField(self):
        playFields = [[Field(0, 0, self.sizeOfField) for x in xrange(self.widthOfField)] for y in xrange(self.heightOfField)]

        for y in range(len(playFields)):
            for x in range(len(playFields[0])):
                playFields[y][x].x = x * playFields[y][x].size*2 + self.xOffset + self.fieldOffset * x
                playFields[y][x].y = y * playFields[y][x].size*2 + self.yOffset + self.fieldOffset * y
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
            if not self.player1.isComputer and self.player2.isComputer:
                self._changePlayerTurn = self._changePlayerTurnArray[1]
            elif not self.player1.isComputer and not self.player2.isComputer:
                self._changePlayerTurn = self._changePlayerTurnArray[0]
            else:
                self._changePlayerTurn = self._changePlayerTurnArray[2]
                self.aiDelay = 0.005
                self.lockdownTime = 0.005
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
        else:
            target.piece.hidden = False
            source.piece.hidden = False
            self.lockdown = True
            self.lockdownTimer = threading.Timer(self.lockdownTime, self._onLockDownFinish,[source,target])
            self.lockdownTimer.start()
        return True

    def win(self,player):
        # music = pyglet.resource.media('sounds/Victory.mp3')
        # musicPlayer = pyglet.media.ManagedSoundPlayer()
        # musicPlayer.queue(music)
        # musicPlayer.play()
        self.window.victoryScreen.victoryPlayer = player
        self.window.currentScreen = self.window.victoryScreen