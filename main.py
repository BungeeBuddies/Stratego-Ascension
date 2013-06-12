#!/usr/bin/python

import pyglet
from pyglet.gl import *
from math import pi, sin, cos
from time import time
from copy import deepcopy
from field import Field
from piece import Piece
from player import Player
from playscreen import PlayScreen
from setupscreen import SetupScreen
from startscreen import StartScreen
from victoryscreen import VictoryScreen
from pyglet.window import Window

class Window(pyglet.window.Window):

    def __init__(self):
        super(Window, self).__init__()
        self.set_size(900, 700)
        self.xOffset = 175
        self.yOffset = 75
        self.fieldOffset = 1
        self.firstClick = True

        self.amountOfPieces = 80
        self.selectedField = None

        self.hoveredButton = None
        self.selectedButton = None

        self.whosTurn = 1
        self.player1 = Player(False, self.createPieceList(), "computer")
        self.player2 = Player(False, self.createPieceList(), "computer")

        self.startScreen = StartScreen(self)
        self.setupScreenP1 = SetupScreen(self.player1, self)
        self.setupScreenP2 = SetupScreen(self.player2, self)
        self.playScreen = PlayScreen(self, self.player1, self.player2)
        self.victoryScreen = VictoryScreen(self)

        self.currentScreen = self.startScreen

        self.fpsLabel = pyglet.text.Label('Empty',
                  font_name='Arial',
                  font_size=8,
                  x=10, y=10,
                  anchor_x='center', anchor_y='center')
        self.last = time()
        self.frames = 0

    def on_key_press(self, symbol, modifiers):
            pass

    def on_mouse_release(self, x, y, button, modifiers):
        if (self.selectedButton is not None):
            self.selectedButton.selected = False

    # def on_mouse_motion(self, x, y, dx, dy):

    #         if (self.hoveredButton is not None):
    #                 if ([self.hoveredButton.x, self.hoveredButton.y] is not [x, y]):
    #                         self.hoveredButton.hover = False

    #         isButton = self.isButton(x, y)
    #         if (isButton is not None):
    #                 isButton.hover = True
    #                 self.hoveredButton = isButton

    def on_mouse_press(self, x, y, button, modifiers):

        isButton = self.isButton(x,y)
        if (isButton is not None):
                self.selectedButton = isButton
                self.selectedButton.selected = True

        clickedField = self.isField(x, y)
        if (clickedField is not None):

            print "Piece pressed: " + str(clickedField.piece)

            # Deselected last field
            if (self.selectedField is not None):
                self.selectedField.selected = False

            # Select new one
            self.selectedField = clickedField
            self.selectedField.selected = True
            self.currentScreen.handleClick(clickedField)

    def isButton(self, x, y):
        if hasattr(self.currentScreen, 'buttons'):
            buttonIndex = 0
            buttonsList = []
            for button in self.currentScreen.buttons:
                    buttonsList.append([button.x,button.y])

            for extraX in range(-self.currentScreen.buttonXSize, self.currentScreen.buttonXSize):
                for extraY in range(-self.currentScreen.buttonYSize, self.currentScreen.buttonYSize):
                    try:
                        buttonIndex = buttonsList.index ([x + extraX,y + extraY])
                    except ValueError:
                        pass
                    else:
                        return self.currentScreen.buttons[buttonIndex]

    def isField(self, x, y):
        if hasattr(self.currentScreen, 'fields'):
        
            fieldIndex = 0
            fieldsList = []

            for field in self.currentScreen.fields:
                fieldsList.append([field.y, field.x])

            fieldSize = self.currentScreen.sizeOfField

            for extraX in range(-fieldSize, fieldSize):
                for extraY in range(-fieldSize, fieldSize):
                    try:
                        fieldIndex = fieldsList.index([y + extraY, x + extraX])
                    except ValueError:
                        pass
                    else:
                        return self.currentScreen.fields[fieldIndex]


                                    

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def drawPoint(self, x, y, color):
        pyglet.graphics.draw(1, GL_POINTS,
                ('v2i', (x, y)),
                ('c3B', (color[0], color[1], color[2])))

    def drawCircle(self, x, y, radius, color):
        smoothness = int(2*radius*pi)
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(color[0], color[1], color[2])
        for i in range(0, smoothness):
                angle = i * pi * 2.0 / smoothness
                glVertex2f(x + radius * cos(angle), y + radius * sin(angle))
        glEnd()

    def createPlayField(self):
        fields = [[Field(0, 0, self.currentScreen.sizeOfField) for x in xrange(self.currentScreen.lengthOfField)] for y in xrange(self.currentScreen.lengthOfField)]

        for y in range(0, len(fields)):
            for x in range(0, len(fields[0])):
                fields[y][x].x = x * fields[y][x].size*2 + self.xOffset + self.fieldOffset * x
                fields[y][x].y = y * fields[y][x].size*2 + self.yOffset + self.fieldOffset * y

        return fields

    def createPieceList(self):
        pieces = []
        #80 pieces, 40 of team a, 40 of team b. I only need to make this list for one player, though
        #Fourty pieces
        
        # One Flag
        for x in range(0,1):
            pieces.append(Piece('F',0))
                        
        # Six Bombs
        for x in range(0,6):
            pieces.append(Piece('B',0))
    
        # One Spy
        for x in range(0,1):
            pieces.append(Piece(1,1))
    
        # Eight Scouts
        for x in range (0,8):
            pieces.append(Piece(2,10))
    
        # Five Miners
        for x in range(0,5):
            pieces.append(Piece(3,1)) 
    
        # Four Sergeants
        for x in range(0,4):
            pieces.append(Piece(4,1))
    
        # Four Lieutenants 
        for x in range(0,4):
            pieces.append(Piece(5,1))
    
        # Four Captains
        for x in range(0,4):
            pieces.append(Piece(6,1))
    
        # Three Majors
        for x in range(0,3):
            pieces.append(Piece(7,1))
    
        # Two Colonels
        for x in range(0,2):
            pieces.append(Piece(8,1))
    
        # One General
        for x in range(0,1):
            pieces.append(Piece(9,1))
    
        # One Marshal
        for x in range(0,1):
            pieces.append(Piece(10,1))
    
        return pieces

    def on_draw(self):
        pass

    def draw_fps(self):
        if time() - self.last >= 1:
                self.fpsLabel.text = str(self.frames)
                self.frames = 0
                self.last = time()
        else:
                self.frames += 1
        self.fpsLabel.draw()

    def update(self, dt):
        glMatrixMode(GL_MODELVIEW)
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        self.draw_fps()
        self.currentScreen.draw()
                
if __name__ == '__main__':
    window = Window()
    pyglet.clock.schedule_interval(window.update, 1.0/60.0)
    pyglet.app.run()
