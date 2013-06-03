#Defines the playfield and then passes it on to the playscreen
import pyglet
import copy
import threading
from pyglet.gl import *
from field import Field
from piece import Piece
from button import Button
from drawer import Drawer

class SetupScreen:
    def __init__(self, player1, player2, window):
        self.window = window
        # self.pieces = pieces
        self.player1 = player1
        self.player2 = player2

        self.widthOfField = 10
        self.heightOfField = 4
        self.sizeOfField = 25
        self.xOffset = self.window.get_size()[0]/4
        self.yOffset = self.window.get_size()[1]/8 + 70

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
                          x=self.window.get_size()[0]/2, y=self.window.get_size()[1]-20,
                          anchor_x='center', anchor_y='center')
        self.footer = pyglet.text.Label('Player ' + str(self.activePlayer) + ', setup your field',
                          font_name='Arial',
                          font_size=16,
                          x=self.window.get_size()[0]/2, y=20,
                          anchor_x='center', anchor_y='center')

    def createArea(self, yOffset, populate):
        fields = [[Field(0, 0, self.sizeOfField) for x in xrange(self.widthOfField)] for y in xrange(self.heightOfField)]
        
        # Create area
        for y in range(0, len(fields)):
            for x in range(0, len(fields[y])):
                fields[y][x].x = x * fields[y][x].size*2 + self.xOffset + self.fieldOffset * x
                fields[y][x].y = y * fields[y][x].size*2 + yOffset + self.fieldOffset * y
                
                if (populate):
                    fields[y][x].piece = self.player1.pieces[y*self.widthOfField+x]

        return fields

    def createButtons(self):
        amountOfButtons = 2
        buttons = [Button(0, 0, self.buttonXSize, self.buttonYSize) for x in xrange(amountOfButtons)]
        buttons[0].label.text = "Done!"
        buttons[0].x = self.window.get_size()[0]/8
        buttons[0].y = self.window.get_size()[1]/4
        buttons[1].label.text = "Autofill"
        buttons[1].x = self.window.get_size()[0]/8*7
        buttons[1].y = self.window.get_size()[1]/4
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
                        #                   |- Height of area * Size of fields*2

            # Check if field is a barrier
            try:
                self.barrierFields.index(n)
            except ValueError:
                pass
            else:
                fields[n].barrier = True
                fields[n].piece = Piece('#', 0)

        return fields


    # def populateField(self):
    #     # Populate bottom area
    #     for y in range(len(self.fields)/2, len(self.fields)):
    #         for x in range(0, len(self.fields[y])):
    #             self.fields[y][x].piece = Piece('', 0)

    #     # Populate top area
    #     for y in range(0, len(self.fields)/2):
    #         for x in range(0,len(self.fields[y])):
    #             self.fields[y][x].piece = self.pieces[y*10+x]

    def handleClick(self, field):
        if (self.firstSelected is None):
            self.firstSelected = field
        elif (self.firstSelected is not field):
            print "second click"
            if (firstSelected.piece is not None):
                field.piece = self.firstSelected.piece
                self.firstSelected.piece = None
            
            self.firstSelected = None

    def draw(self):
        self.header.draw()
        self.footer.draw()

        for area in [self.bottomArea, self.topArea]:
            for y in range(0, len(area)):
                for field in area[y]:
     
                    # if field.selected:
                        
                    #     #  If not selected
                    #     if self.firstSelected is None:
                    #         if field.piece.type != '':
                    #             self.firstSelected = field
                    #     else: 

                    #         # If empty field
                    #         if field.piece.type == '':
                    #             field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
                    #             self.firstSelected.piece = Piece('', 0)
                    #         else:
                    #             if field.piece.type != self.firstSelected.piece.type:
                    #                 helpPiece = self.firstSelected.piece
                    #                 self.firstSelected.piece = field.piece
                    #                 field.piece = helpPiece
                    #         self.firstSelected = None

                    # field.selected = False
                    
                    # if field is self.firstSelected:
                    #     glColor3f(1, 0, 1)
                    # else:
                    #     glColor3f(1, 1, 1)

                    if (field is self.firstSelected):
                        glColor3f(1, 0, 1)
                    elif (field.selected):
                        glColor3f(1, 1, 0)
                    else:
                        glColor3f(1, 1, 1)

                    Drawer.drawField(field)

            for field in self.barriers:
                glColor3f(1, 0, 0)
                Drawer.drawField(field)

        glColor3f(1, 1, 1)
        if self.buttons[0].selected:
            # self.buttons[0].selected = False
            if  not self.checkIfDone():
                self.footer.text = "You have to place all your pieces before you can continue"
                # Reset footer text to original after x seconds
                if hasattr(self, 'textResetTimer') and self.textResetTimer.isAlive():
                    self.textResetTimer.cancel()
                    self.textResetTimer.join()
                self.textResetTimer = threading.Timer(3, self.resetBottomText)
                self.textResetTimer.start()
        if self.buttons[1].selected:
            self.autofill()
            # self.buttons[1].selected = False
        for button in self.buttons:
            Drawer.drawButton(button)

    def checkIfDone(self):
        # If there still are pieces in the bottom field, return false
        for y in range(0,len(self.fields)/2):
            for x in range(0,len(self.fields[y])):
                if self.fields[y][x].piece.type != '':
                    return False

        self.activePlayer += 1
        self.resetBottomText()

        # Fill pieces for player 1
        if self.activePlayer == 2:
            for y in xrange(len(self.fields)/2, len(self.fields)):
                for x in xrange(0, len(self.fields[y])):
                    self.window.playScreen.fields[len(self.window.playScreen.fields) + len(self.fields)/2 - y - 1][len(self.fields[y])-x-1].piece = self.fields[y][x].piece
                    self.window.playScreen.player1Pieces.append(self.fields[y][x].piece)
        # Fill pieces for player 2
        else:
            for y in xrange(len(self.fields)/2, len(self.fields)):
                for x in xrange(0, len(self.fields[y])):
                    self.window.playScreen.fields[-len(self.fields)/2 + y][x].piece = self.fields[y][x].piece
                    self.window.currentScreen = self.window.playScreen
                    self.window.playScreen.player2Pieces.append(self.fields[y][x].piece)
        
        # self.populateField()
        
        return True         

    def resetBottomText(self):
        self.footer.text = 'Player ' + str(self.activePlayer) + ', setup your field'

    def autofill(self):
        regels = self.fields[:len(self.fields)/2]
        emptyfields = [f for r in regels for f in r if f.piece.type != '']
        topping = self.fields[len(self.fields)/2:]
        tobefilledfields = [f for r in topping for f in r if f.piece.type == '']
        for (a, b) in zip(emptyfields, tobefilledfields):
            b.piece = a.piece
            a.piece = Piece('', 0)