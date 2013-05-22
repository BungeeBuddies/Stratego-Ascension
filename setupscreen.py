#Defines the playfield and then passes it on to the playscreen
import pyglet
import copy
from pyglet.gl import *
from field import Field
from piece import Piece


class SetupScreen:
	def __init__(self,pieces,window):
		self.window = window
		self.pieces = pieces
		
		self.widthOfField = 10
		self.heightOfField = 8
		self.sizeOfField = 25
		self.xOffset = self.window.get_size()[0]/4
		self.yOffset = self.window.get_size()[1]/8 + 70
		self.extraYOffset = 25
		self.fieldOffset = 1
		self.sizeOfButton = 50
		self.fields = self.createStartField()
		self.extraFields = self.setupExtraFields()

		self.populateField()
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

	def createStartField(self):
		fields = [[Field(0, 0, self.sizeOfField) for x in xrange(self.widthOfField)] for y in xrange(self.heightOfField)]
		for y in range(0, len(fields)/2):
			for x in range(0, len(fields[y])):
				fields[y][x].x = x * fields[y][x].size*2 + self.xOffset + self.fieldOffset * x
				fields[y][x].y = y * fields[y][x].size*2 + self.yOffset + self.fieldOffset * y
		for y in range(len(fields)/2,len(fields)):
			for x in range(0,len(fields[y])):
				fields[y][x].x = x * fields[y][x].size*2 + self.xOffset + self.fieldOffset * x
				fields[y][x].y = y * fields[y][x].size*2 + self.yOffset + self.extraYOffset + self.fieldOffset * y
		fields[0].append(Field(0,0,100))
		return fields

	def setupExtraFields(self):
		fields = [Field(0, 0, self.sizeOfField) for x in xrange(self.widthOfField)]

		for n in range(0, len(fields)):
			fields[n].x = n * fields[n].size*2 + self.xOffset + self.fieldOffset * n
			fields[n].y = len(self.fields) * fields[n].size*2 + self.yOffset + self.extraYOffset  + self.fieldOffset * len(self.fields)
		return fields


	def populateField(self):
		for y in range(len(self.fields)/2,len(self.fields)):
			for x in range(0,len(self.fields[y])):
				self.fields[y][x].piece = Piece('')
		for y in range(0,len(self.fields)/2):
			for x in range(0,len(self.fields[y])):
				self.fields[y][x].piece = self.pieces[y*10+x]
		self.extraFields[2].piece = self.extraFields[3].piece = self.extraFields[6].piece = self.extraFields[7].piece = Piece('#') 


	def draw(self):
		self.checkIfDone()
		self.header.draw()
		self.footer.draw()
		for y in range(0, len(self.fields)):
			for field in self.fields[y]:
				if (field.selected):
					if (self.firstSelected is None):
						if field.piece.type != '':
							self.firstSelected = field
					else: 
						if (field.piece.type == ''):
							field.piece = Piece(self.firstSelected.piece.type)
							self.firstSelected.piece = Piece('')
						self.firstSelected = None
				field.selected = False
				if (field is self.firstSelected):
					glColor3f(1, 0, 1)
				else:
					glColor3f(1, 1, 1)
				self.drawField(field)

		for field in self.extraFields:
			glColor3f(1, 0, 0)
			self.drawField(field)

				

	def drawField(self,field):
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
		field.label.draw()

	def checkIfDone(self):
		for y in range(0,len(self.fields)/2):
			for x in range(0,len(self.fields[y])):
				if self.fields[y][x].piece.type != '':
					return
		self.activePlayer += 1
		if self.activePlayer == 2:
			for y in range(len(self.fields)/2,len(self.fields)):
				for x in range(0,len(self.fields[y])):
					self.window.playScreen.fields[x][y] = self.fields[x][y]
		self.populateField()