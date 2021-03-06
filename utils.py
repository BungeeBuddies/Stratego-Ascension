import pyglet
from pyglet.gl import *
from field import Field

class Utils(object):

    @staticmethod
    def drawField(field):

        if (field.selected):
            glColor3f(1, 0, 1)

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

        if (field.piece is not None):
            piece = field.piece

            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glBegin(GL_QUADS)
            # Top left
            glVertex2f(field.x + piece.size, field.y + piece.size)
            # Top right
            glVertex2f(field.x - piece.size, field.y + piece.size)
            # Bottom right
            glVertex2f(field.x - piece.size, field.y - piece.size)
            # Bottom left
            glVertex2f(field.x + piece.size, field.y - piece.size)
            glEnd()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            field.label.draw()

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

    @staticmethod
    def getFieldIndex(piece, fields):
        for y in xrange(0,len(fields)):
            for x in xrange(0,len(fields[y])):
                if fields[y][x].piece is piece:
                    return[y,x]
    # @staticmethod
    # def getField(self, x, y, fields):
    
    @staticmethod
    def isLegalMove(source, target, fields):
        #check if the target field is a barrier
        if target.piece is not None and target.piece.type == '#':
            return False    
        sourceX = None
        sourceY = None
        targetX = None
        targetY = None
        for i, x in enumerate(fields):
            if source in x:
                sourceY = i
                sourceX = x.index(source)
            if target in x:
                targetY = i
                targetX = x.index(target)
        if source.piece is not None:
            if sourceX == targetX or sourceY == targetY: # Both fields are on the same line
                delta = (sourceY - targetY if sourceX == targetX  else sourceX - targetX) # The difference between the fields                    
                if abs(delta) <= source.piece.steps: # Check if the piece can move this far
                    # If the piece can move more than 1 space
                    if source.piece.steps > 1:                            
                        # Finally: Check if something is in between (only applies if piece can set more then one step)
                        if sourceX == targetX:  # Check if the source and target are on the same row                                
                            # If the target field is above the source, start at the field above else at the field below
                            step = -1 if sourceY > targetY else 1                                 
                            # Check if all fields until the target are empty
                            for y in xrange(sourceY+step, targetY, step):
                                if fields[y][sourceX].piece is not None:
                                    return False                            
                        # Check if the source and target are one the same column
                        else:
                            step = -1 if sourceX > targetX else 1 # Same as above
                            for x in xrange(sourceX+step, targetX, step):
                                if fields[sourceY][x].piece is not None:
                                    return False                      
                    return True
            return False