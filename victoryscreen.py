import pyglet
import sys
from pyglet.gl import *
from field import Field
from button import Button
from utils import Utils

class VictoryScreen(object):

    def __init__(self, window):
        self.window = window
        self.width = 900
        self.height = 700
        self.xOffset = self.width/4
        self.yOffset = self.height/8 + 35
        self.buttonXSize = 50
        self.buttonYSize = 25
        self.victoryPlayer = None 
        self.buttons = self.createButtons()
        
    def createButtons(self):
        amountOfButtons = 3
        buttons = [Button(0, 0, self.buttonXSize,self.buttonYSize) for x in xrange(amountOfButtons)]
        buttons[0].label.text = "<font face=\"Arial\" color=\"white\" size=\"16\">Rematch</font>"
        buttons[0].label.font_size = 9
        buttons[0].x = self.width/8
        buttons[0].y = self.height-400
        buttons[1].label.text = "<font face=\"Arial\" color=\"white\" size=\"16\">Main menu</font>"
        buttons[1].label.font_size = 9
        buttons[1].x = self.width/2
        buttons[1].y = self.height-400
        buttons[2].label.text = "<font face=\"Arial\" color=\"white\" size=\"16\">Exit game </font>"
        buttons[2].label.font_size = 9
        buttons[2].x = self.width/8*7
        buttons[2].y = self.height-400

        return buttons
    

        
    def draw(self):
        if self.buttons[0].selected:
            self.buttons[0].selected = False
            self.window.resetWindows()
            self.window.currentScreen = self.window.setupScreenP1
        if self.buttons[1].selected:
            self.window.resetWindows()
            self.window.currentScreen = self.window.startScreen
            self.buttons[1].selected = False
        if self.buttons[2].selected:
            sys.exit()
        for button in self.buttons:
            Utils.drawButton(button)
        pyglet.text.Label(self.victoryPlayer.name + ' has won!',
                  font_name='Arial',
                  font_size=30,
                  x=self.width/2, y= self.height-200,
                  anchor_x='center', anchor_y='center').draw()