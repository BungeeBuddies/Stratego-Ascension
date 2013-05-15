#Defines the playfield and then passes it on to the playscreen
import pyglet
import copy
from pyglet.gl import *
from field import Field


class StartScreen:
	def __init__(self,pieces,window):
		self.window = window
		self.pieces = pieces
		
		self.widthOfField = 10
		self.heightOfField = 8
		self.sizeOfField = 25
		self.xOffset = self.window.get_size()[0]/4
		self.yOffset = self.window.get_size()[1]/8 + 70
		self.fieldOffset = 1
		self.sizeOfButton = 50
		self.fields = self.createStartField()

		self.populateField()
		self.bottomText = 'Player 1, setup your field'
		self.firstSelected = None
		self.secondSelected = None

	def createStartField(self):
		fields = [[Field(0, 0, self.sizeOfField) for x in xrange(self.widthOfField)] for y in xrange(self.heightOfField)]
		for y in range(0, len(fields)/2):
			for x in range(0, len(fields[y])):
				fields[y][x].x = x * fields[y][x].size*2 + self.xOffset + self.fieldOffset * x
				fields[y][x].y = y * fields[y][x].size*2 + self.yOffset + self.fieldOffset * y
		yOffset = self.yOffset + 25
		for y in range(len(fields)/2,len(fields)):
			for x in range(0,len(fields[y])):
				fields[y][x].x = x * fields[y][x].size*2 + self.xOffset + self.fieldOffset * x
				fields[y][x].y = y * fields[y][x].size*2 + yOffset + self.fieldOffset * y
		return fields

	def populateField(self):
		for y in range(0,len(self.fields)/2):
			for x in range(0,len(self.fields[y])):
				field = self.fields[y][x]
				field.piece = self.pieces[y*10+x]


	def draw(self):
		self.window.clear()
		pyglet.text.Label('Start Screen',
                          font_name='Arial',
                          font_size=16,
                          x=self.window.get_size()[0]/2, y=self.window.get_size()[1]-20,
                          anchor_x='center', anchor_y='center').draw()

		pyglet.text.Label('This side is looking at the enemy',
                          font_name='Arial',
                          font_size=16,
                          x=self.window.get_size()[0]/2, y=self.window.get_size()[1]-60,
                          anchor_x='center', anchor_y='center').draw()

		pyglet.text.Label(self.bottomText,
                          font_name='Arial',
                          font_size=16,
                          x=self.window.get_size()[0]/2, y=20,
                          anchor_x='center', anchor_y='center').draw()

		for y in range(0, len(self.fields)):
			for field in self.fields[y]:

				if (field.selected):
					if (self.firstSelected is None):
						self.firstSelected = field
					else: 
						if (field.piece.type == ''):
							field.piece.type = self.firstSelected.piece.type
							self.firstSelected.piece.type = ''
						self.firstSelected = None
				field.selected = False
				if (field is self.firstSelected):
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

				#draw the Label
				pyglet.text.Label(str(field.piece.type),
                          font_name='Arial',
                          font_size=16,
                          x=field.x, y=field.y,
                          anchor_x='center', anchor_y='center').draw()