#Defines the playfield and then passes it on to the playscreen
import pyglet
import copy
import threading
import random
from copy import copy
from pyglet.gl import *
from field import Field
from piece import Piece
from button import Button
from utils import Utils

class SetupScreen:

    def __init__(self, player, window):
        self.window = window
        self.width = 900
        self.height = 700
        self.player = player

        self.widthOfField = 10
        self.heightOfField = 4
        self.sizeOfField = 25

        self.isDone = False
        self.xOffset = self.width/4
        self.yOffset = self.height/8 + 70


        # Space between bottom and top field
        self.fieldOffset = 1

        self.bottomArea = self.createArea(self.yOffset, True)
        self.betweenAreasYOffset = self.bottomArea[-1][-1].y + self.bottomArea[-1][-1].size*2 + 25
        
        self.topArea = self.createArea(self.betweenAreasYOffset, False)
        self.fields = [item for sublist in self.topArea for item in sublist] + [item for sublist in self.bottomArea for item in sublist]

        self.barrierFields = [2, 3, 6, 7]
        self.barriers = self.setupBarriers()

        self.buttonXSize = 50
        self.buttonYSize = 25

        self.buttons = self.createButtons()

        self.activePlayer = 1
        self.firstSelected = None

        self.header = pyglet.text.Label('Setup Screen',
                           font_name='Arial',
                          font_size=16,
                          x=self.width/2, y=self.height-20,
                          anchor_x='center', anchor_y='center')

        self.footer = pyglet.text.Label('Player ' + str(self.activePlayer) + ', setup your field',
                          font_name='Arial',
                          font_size=16,
                          x=self.width/2, y=20,
                          anchor_x='center', anchor_y='center')

    def createArea(self, yOffset, populate):
        fields = [[Field(0, 0, self.sizeOfField) for x in xrange(self.widthOfField)] for y in xrange(self.heightOfField)]
        
        # Create area
        for y in range(0, len(fields)):
            for x in range(0, len(fields[y])):
                fields[y][x].x = x * fields[y][x].size*2 + self.xOffset + self.fieldOffset * x
                fields[y][x].y = y * fields[y][x].size*2 + yOffset + self.fieldOffset * y
                
                if (populate):
                    fields[y][x].piece = self.player.pieces[y][x]
                    # fields[y][x].piece.field = fields[y][x]

        return fields

    def createButtons(self):
        amountOfButtons = 2
        buttons = [Button(0, 0, self.buttonXSize, self.buttonYSize) for x in xrange(amountOfButtons)]
        buttons[0].label.text = "Done!"
        buttons[0].x = self.width/8
        buttons[0].y = self.height/4
        buttons[1].label.text = "Autofill"
        buttons[1].x = self.width/8*7
        buttons[1].y = self.height/4
        return buttons

    # Barriers
    def setupBarriers(self):
        fields = [Field(0, 0, self.sizeOfField) for x in xrange(self.widthOfField)]

        for n in range(0, len(fields)):
            fields[n].x = n * fields[n].size*2 + self.xOffset + self.fieldOffset * n
            
            fields[n].y = (len(self.topArea) * fields[n].size*2) + self.betweenAreasYOffset + (self.fieldOffset * len(self.topArea))
                        # |-----------------Y------------------|   |----------Y-----------|   |---------Y--------------------------|
                        #                   |                                 |                         |- + (Offset between fields)
                        #                   |                                 |- + Distance between top and bottom areas
                        #                   |- Number of fields in height of top area * Size of fields*2

            # Check if field is a barrier
            try:
                self.barrierFields.index(n)
            except ValueError:
                pass
            else:
                fields[n].barrier = True
                fields[n].piece = Piece('#', 0)

        return fields

    def handleClick(self, field):
        if (self.firstSelected is None):
            self.firstSelected = field

        elif (self.firstSelected is not field):
            if (self.firstSelected.piece is not None):
                field.piece = self.firstSelected.piece
                self.firstSelected.piece = None
                
            self.firstSelected = None

    def draw(self):

        if (self.player.isComputer):
            self.fillTopArea()
            self.isDone = True
        if self.isDone:
            if self is self.window.setupScreenP2:
                self.window.currentScreen = self.window.playScreen
            else: 
                self.window.currentScreen = self.window.setupScreenP2
        else:
            self.header.draw()
            self.footer.draw()

            for area in [self.bottomArea, self.topArea]:
                for y in range(0, len(area)):
                    for field in area[y]:
         
                        if (field is self.firstSelected):
                            glColor3f(1, 0, 1)
                        else:
                            glColor3f(1, 1, 1)

                        Utils.drawField(field)

                for field in self.barriers:
                    glColor3f(1, 0, 0)
                    Utils.drawField(field)

            glColor3f(1, 1, 1)
            if self.buttons[0].selected:
                self.buttons[0].selected = False
                if  not self.checkIfDone():
                    self.footer.text = "You have to place all your pieces before you can continue"
                    # Reset footer text to original after x seconds
                    if hasattr(self, 'textResetTimer') and self.textResetTimer.isAlive():
                        self.textResetTimer.cancel()
                        self.textResetTimer.join()
                    self.textResetTimer = threading.Timer(3, self.resetBottomText)
                    self.textResetTimer.start()
                else:
                    self.player.pieces = self.topArea
                    self.isDone = True
            if self.buttons[1].selected:
                self.autofill()
                self.buttons[1].selected = False
            for button in self.buttons:
                Utils.drawButton(button)

    def checkIfDone(self):
        # If there still are pieces in the bottom field, return false
        for y in range(0, len(self.bottomArea)):
            for x in range(0, len(self.bottomArea[y])):
                if self.bottomArea[y][x].piece is not None:
                    return False       
        return True         

    def resetBottomText(self):
        self.footer.text = 'Player ' + str(self.activePlayer) + ', setup your field'

    def fillTopArea(self):
        tempArray = list([item for sublist in self.bottomArea for item in sublist])
        random.shuffle(tempArray)

        for row in range(0, len(self.topArea)):
            for field in range(0, len(self.topArea[row])):
                self.topArea[row][field].piece = copy(tempArray[row*self.widthOfField+field].piece)

    def autofill(self):
        if (not self.checkIfDone()):
            self.fillTopArea()
            for row in range(0, len(self.bottomArea)):
                for field in range(0, len(self.bottomArea[row])):
                    self.bottomArea[row][field].piece = None
        else:
            self.fillTopArea()
