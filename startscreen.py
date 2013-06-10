import pyglet
from pyglet.gl import *
from field import Field
from button import Button

class StartScreen:

    def __init__(self, window):
        self.window = window
        self.width = window.get_size()[0]
        self.height = window.get_size()[1]
        self.xOffset = self.window.get_size()[0]/4
        self.yOffset = self.window.get_size()[1]/8 + 35

        self.buttonXSize = 50
        self.buttonYSize = 25

        self.buttons = self.createButtons()
        
    def createButtons(self):
        amountOfButtons = 2
        buttons = [Button(0, 0, self.buttonXSize,self.buttonYSize) for x in xrange(amountOfButtons)]
        buttons[0].label.text = "<font face=\"Arial\" color=\"white\" size=\"16\">Player vs Player</font>"
        buttons[0].label.font_size = 9
        buttons[0].x = self.window.get_size()[0]/8
        buttons[0].y = self.window.get_size()[1]/4
        buttons[1].label.text = "<font face=\"Arial\" color=\"white\" size=\"16\">Player vs Computer</font>"
        buttons[1].label.font_size = 9
        buttons[1].x = self.window.get_size()[0]/8*7
        buttons[1].y = self.window.get_size()[1]/4
        return buttons
    

        
    def draw(self):
        if self.buttons[0].selected:
            # self.buttons[0].selected = False
            self.window.currentScreen = self.window.setupScreenP1
        if self.buttons[1].selected:
            self.window.currentScreen = self.window.setupScreenP1
            # self.buttons[1].selected = False
        for button in self.buttons:
            self.drawButton(button)
            
        pyglet.text.Label('Stratego-Ascension',
                          font_name='Arial',
                          font_size=30,
                          x=self.width/2, y= self.height-200,
                          anchor_x='center', anchor_y='center').draw()



                        
    def drawButton(self,button):

        offset = 0
        if (button.selected):
            offset = 0.1

        # Button area
        if (button.hover):      
            glColor3f(1, 0, 0)
        else:
            glColor3f(0.8, 0, 0)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glBegin(GL_QUADS)
        # Top left
        glVertex2f(button.x - button.xSize * (1.0 + offset), button.y + button.ySize * (1.0 + offset))
        # Top right
        glVertex2f(button.x + button.xSize * (1.0 - offset), button.y + button.ySize * (1.0 + offset))
        # Bottom right
        glVertex2f(button.x + button.xSize * (1.0 - offset), button.y - button.ySize * (1.0 - offset))
        # Bottom left
        glVertex2f(button.x - button.xSize * (1.0 + offset), button.y - button.ySize * (1.0 - offset))
        glEnd()

        

        # Button 3D Top
        glColor3f(0.5, 0, 0)
        glBegin(GL_QUADS)
        # Top left
        glVertex2f(button.x - button.xSize * 1.2, button.y + button.ySize * 1.2)
        # Top right
        glVertex2f(button.x + button.xSize * 0.8, button.y + button.ySize * 1.2)
        # Bottom right
        glVertex2f(button.x + button.xSize * (1.0 - offset), button.y + button.ySize * (1.0 + offset))
        # Bottom left
        glVertex2f(button.x - button.xSize * (1.0 - offset), button.y + button.ySize * (1.0 + offset))
        glEnd()

        # Button 3D Left
        glColor3f(0.5, 0, 0)
        glBegin(GL_QUADS)
        # Top left
        glVertex2f(button.x - button.xSize * 1.2, button.y + button.ySize * 1.2)
        # Top right
        glVertex2f(button.x - button.xSize * (1.0 + offset), button.y + button.ySize * (1.0 + offset))
        # Bottom right
        glVertex2f(button.x - button.xSize * (1.0 + offset), button.y - button.ySize * (1.0 - offset))
        # Bottom left
        glVertex2f(button.x - button.xSize * 1.2, button.y - button.ySize * 0.8)
        glEnd()

        glColor3f(1, 1, 1)

        #draw the Label
        button.label.draw()
