import pyglet
from pyglet.gl import *
from field import Field
from button import Button
from utils import Utils

class StartScreen:

    def __init__(self, window):
        self.window = window
        self.width = 900
        self.height = 700
        self.xOffset = self.width/4
        self.yOffset = self.height/8 + 35

        self.buttonXSize = 50
        self.buttonYSize = 25

        self.buttons = self.createButtons()
        
    def createButtons(self):
        amountOfButtons = 3
        buttons = [Button(0, 0, self.buttonXSize,self.buttonYSize) for x in xrange(amountOfButtons)]
        buttons[0].label.text = "<font face=\"Arial\" color=\"white\" size=\"16\">Player vs Player</font>"
        buttons[0].label.font_size = 9
        buttons[0].x = self.width/8
        buttons[0].y = self.height/8
        buttons[1].label.text = "<font face=\"Arial\" color=\"white\" size=\"16\">Player vs Computer</font>"
        buttons[1].label.font_size = 9
        buttons[1].x = self.width/8*7
        buttons[1].y = self.height/8
        buttons[2].label.text = "<font face=\"Arial\" color=\"white\" size=\"16\">Computer vs Computer</font>"
        buttons[2].label.font_size = 9
        buttons[2].x = self.width/8*4
        buttons[2].y = self.height/8
        return buttons
    

        
    def draw(self):
        if self.buttons[0].selected: #PvP
            self.buttons[0].selected = False
            self.window.player1.isComputer = False
            self.window.player1.name = "Player 1"
            self.window.player2.isComputer = False
            self.window.player2.name = "Player 2"
            self.window.setupScreenP1.resetBottomText()
            self.window.setupScreenP2.resetBottomText()
            self.window.currentScreen = self.window.setupScreenP1
        elif self.buttons[1].selected: #PvPC
            self.window.player1.isComputer = False
            self.window.player1.name = "Player"
            self.window.player2.isComputer = True
            self.window.player2.name = "Computer"
            self.window.setupScreenP1.resetBottomText()
            self.window.currentScreen = self.window.setupScreenP1
            self.buttons[1].selected = False
        elif self.buttons[2].selected: #PCvPC
            self.window.player1.isComputer = True
            self.window.player1.name = "Computer 1"
            self.window.player2.isComputer = True
            self.window.player2.name = "Computer 2"
            self.window.currentScreen = self.window.setupScreenP1
            self.buttons[2].selected = False
        else:
            for button in self.buttons:
                Utils.drawButton(button)              
            pyglet.text.Label('Stratego-Ascension',
                              font_name='Arial',
                              font_size=30,
                              x=self.width/2, y= self.height-200,
                              anchor_x='center', anchor_y='center').draw()