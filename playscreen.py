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
        self.playersTurn = None

        self.widthOfField = 10
        self.heightOfField = 10
        self.sizeOfField = 25
        self.isFieldSelected = False
        self.selectedField = 0
        self.color = [1, 1, 1]

        self.aiDelay = 0.5

        self.visibleEnemy = None
        self.lockDownTime = 0.5
        self.lockDown = False
        self.firstSelectedXPosition = None
        self.firstSelectedYPosition = None
        self.playFields = self.createPlayField()
        self.fields = [item for sublist in self.playFields for item in sublist]

        self.selectedField = None
        self.firstSelected = None
        

        
    def handleClick(self, field):
        #if the currentPlayer is a computer, ignore all of this. Also ignore if lockdown is true
        if self.playersTurn.isComputer or self.lockDown:
            return
        #Firstclick: check if no piece has been selected before and if there is a piece there, and if this piece is his. If all of this is true, then check if he clicked a piece which can move.
        if self.firstSelected is None and field.piece is not None:
            if field.piece.steps > 0 and field.piece.owner == self.playersTurn:
                self.firstSelected = field
        elif (self.firstSelected is not None): 
            if (field is self.firstSelected):
                self.firstSelected = None
            elif (Utils.isLegalMove(self.firstSelected, field, self.playFields)): #if the move is legal, execute it
                self.executeMove(self.firstSelected, field)
                            


    def onLockDownFinish(self, source, target):
        # field = self.visibleEnemy       
        # win = False
        # win = Utils.attack(source, target)
        
        # print "lolololol"
        
        # if (win):
        #     self.window.victoryScreen.victoryPlayer = self.playersTurn
        #     self.window.currentScreen = self.window.victoryScreen

        self.changePlayerTurn()
        self.lockDown = False   

    def changePlayerTurn(self):
        self.firstSelected = None
        self.visibleEnemy = None
        lastPlayer = None

        if self.playersTurn is None:
            self.playersTurn = self.player1
            lastPlayer = self.player2
        
        elif self.playersTurn == self.player1:
            self.playersTurn = self.player2
            lastPlayer = self.player1
        
        else:
            self.playersTurn = self.player1
            lastPlayer = self.player2

        # # Hide last player's pieces
        # for row in lastPlayer.pieces:
        #     for piece in row:
        #         piece.hidden = True

        # # Reveal current player's pieces
        # for row in self.playersTurn.pieces:
        #     for piece in row:
        #         piece.hidden = False

        if self.init:
            if self.playersTurn.isComputer:
                # print "Computer playing"
                win = self.playersTurn.play(self.playFields)
                
                if win:
                    self.window.victoryScreen.victoryPlayer = "1" if self.playersTurn is self.player1 else "2"
                    self.window.currentScreen = self.window.victoryScreen

                threading.Timer(0.1, self.changePlayerTurn).start()

    def createPlayField(self):
        playFields = [[Field(0, 0, self.sizeOfField) for x in xrange(self.widthOfField)] for y in xrange(self.heightOfField)]

        for y in range(len(playFields)):
            for x in range(len(playFields[0])):
                playFields[y][x].x = x * playFields[y][x].size*2 + self.xOffset + self.fieldOffset * x
                playFields[y][x].y = y * playFields[y][x].size*2 + self.yOffset + self.fieldOffset * y
                if (y in range(4)):
                    playFields[y][x].piece = self.player1.pieces[y][x]
                if (y in range(6, 10)):
                    playFields[y][x].piece = self.player2.pieces[y-6][x]

                try:
                    self.barrierFields.index([x, y])
                except ValueError:
                    pass
                else:
                    playFields[y][x].barrier = True
                    playFields[y][x].piece = Piece('#', 0)

        return playFields

    def draw(self):

        if (not self.init):
            self.init = True
            self.changePlayerTurn()
            # threading.Timer(0.5, self.playersTurn.play).start()

        pyglet.text.Label('Player 1',
                          font_name='Arial',
                          font_size=16,
                          x=self.width/2, y=self.height-20,
                          anchor_x='center', anchor_y='center').draw()

        pyglet.text.Label('Player 2',
                          font_name='Arial',
                          font_size=16,
                          x=self.width/2, y=20,
                          anchor_x='center', anchor_y='center').draw()
        
        # Draw playFields
                    #         self.hiddenField.x = field.x
                    # self.hiddenField.y = field.y
                    # self.hiddenField.size = field.size
                    # self.hiddenField.piece.owner = field.piece.owner
                    # field = self.hiddenField
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

    def executeMove(self,source, target):
        #check if its a legal move
        Utils.isLegalMove(source, target, self.playFields)
        pass
        # if self.firstSelected.piece.owner is not field.piece.owner:
        #                        self.visibleEnemy = field
        #                        self.lockDown = True
        #                        field.piece.hidden = False
        #                        self.textResetTimer = threading.Timer(self.lockDownTime, self.onLockDownFinish, 
        #                                                                 [self.firstSelected, field])
        #                        self.textResetTimer.start()
                    
        #             else:
        #                 field.piece = self.firstSelected.piece
        #                 self.firstSelected.piece = None
        #                 self.changePlayerTurn()

        #     self.firstSelected = None