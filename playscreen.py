import pyglet
from pyglet.gl import *
from field import Field

class PlayScreen:

	def __init__(self, window):
		self.window = window
		self.xOffset = self.window.get_size()[0]/4
		self.yOffset = self.window.get_size()[1]/8 + 35
		self.fieldOffset = 1

		self.lengthOfField = 10
		self.sizeOfField = 25
		self.isFieldSelected = False
		self.selectedField = 0
		self.fields = self.createPlayField()


	def createPlayField(self):
		fields = [[Field(0, 0, self.sizeOfField) for x in xrange(self.lengthOfField)] for y in xrange(self.lengthOfField)]

		for y in range(0, len(fields)):
			for x in range(0, len(fields[0])):
				fields[y][x].x = x * fields[y][x].size*2 + self.xOffset + self.fieldOffset * x
				fields[y][x].y = y * fields[y][x].size*2 + self.yOffset + self.fieldOffset * y

		return fields

	def draw(self):
		pyglet.text.Label('Player 1',
                          font_name='Arial',
                          font_size=16,
                          x=self.window.get_size()[0]/2, y=self.window.get_size()[1]-20,
                          anchor_x='center', anchor_y='center').draw()

		pyglet.text.Label('Player 2',
                          font_name='Arial',
                          font_size=16,
                          x=self.window.get_size()[0]/2, y=20,
                          anchor_x='center', anchor_y='center').draw()

		for y in range(0, len(self.fields)):
			for field in self.fields[y]:

				if (field.selected):
					glColor3f(1, 0, 1)
				else:
					glColor3f(1, 1, 1)

				# Draw center
				# self.drawCircle(field.x, field.y, 5, [1, 1, 1])

				# # Draw top side
				pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', 
    				(field.x + field.size, field.y + field.size, 
    				field.x - field.size, field.y + field.size)))

				# Draw down side
				pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', 
    				(field.x + field.size, field.y - field.size, 
    				field.x - field.size, field.y - field.size)))
				
				# Draw left side
				pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', 
    				(field.x - field.size, field.y - field.size,
    				field.x - field.size, field.y + field.size)))

				# Draw right side
				pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', 
    				(field.x + field.size, field.y - field.size,
    				field.x + field.size, field.y + field.size)))