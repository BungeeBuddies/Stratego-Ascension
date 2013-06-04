import pyglet
from pyglet.gl import *
from field import Field

class Drawer(object):

    @staticmethod
    def drawField(field):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_QUADS)
        # Top left
        glVertex2f(field.x + field.size, field.y + field.size)
        # Top right
        glVertex2f(field.x - field.size, field.y + field.size)
        # Bottom right
        glVertex2f(field.x - field.size, field.y - field.size)
        # Bottom left
        glVertex2f(field.x + field.size, field.y - field.size)
        glEnd()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        if (field.piece is not None and field.piece.label is not None):
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glBegin(GL_QUADS)
            # Top left
            glVertex2f(field.x + field.piece.size, field.y + field.piece.size)
            # Top right
            glVertex2f(field.x - field.piece.size, field.y + field.piece.size)
            # Bottom right
            glVertex2f(field.x - field.piece.size, field.y - field.piece.size)
            # Bottom left
            glVertex2f(field.x + field.piece.size, field.y - field.piece.size)
            glEnd()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            
            field.piece.label.draw()

    @staticmethod
    def drawButton(button):
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
