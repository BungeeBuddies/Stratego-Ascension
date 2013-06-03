import pyglet
from pyglet.gl import *
from field import Field
from piece import Piece
from drawer import Drawer

class PlayScreen:

	def __init__(self, window):
		self.window = window
		self.xOffset = self.window.get_size()[0]/4
		self.yOffset = self.window.get_size()[1]/8 + 35
		self.fieldOffset = 1
		self.barrierFields = [[2, 4], [3, 4], [6, 4], [7, 4], [2, 5], [3, 5], [6, 5], [7, 5]]

		self.widthOfField = 10
		self.heightOfField = 10
		self.sizeOfField = 25
		self.isFieldSelected = False
		self.selectedField = 0
		self.color = [1, 1, 1]
		self.fields = self.createPlayField()
		self.selectedField = None
		self.player1Pieces = []
		self.player2Pieces = [] 
		self.firstSelected = None
		
		

	#def checkPlayField(self):
		
	def createPlayField(self):
		fields = [[Field(0, 0, self.sizeOfField) for x in xrange(self.widthOfField)] for y in xrange(self.heightOfField)]

		for y in range(0, len(fields)):
			for x in range(0, len(fields[0])):
				fields[y][x].x = x * fields[y][x].size*2 + self.xOffset + self.fieldOffset * x
				fields[y][x].y = y * fields[y][x].size*2 + self.yOffset + self.fieldOffset * y
				try:
					self.barrierFields.index([x, y])
				except ValueError:
					pass
				else:
					fields[y][x].barrier = True
					fields[y][x].piece = Piece('#',0)

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
		# Draw fields
		for y in range(0, len(self.fields)):
			for x in range( 0,len(self.fields[y])):				
				field = self.fields[y][x]
				if field.selected:				
					if self.firstSelected is None:
						if field.piece.type != '' and field.piece.type is not 'F' and field.piece.type is not'B' and field.piece.type is not '#':
								self.firstSelected = field
					elif self.firstSelected is not field: 
						#TODO check if the player can take this amount of steps
						if field.piece.type == '#':
							print "blokkade"
						elif field.piece.type == 10:
							if self.firstSelected.piece.type == 1:
								print('Spy =D')
								field.piece = self.firstSelected.piece
								self.firstSelected.piece = Piece('', 0)
						elif field.piece.type == 'B':
							if self.firstSelected.piece.type == 3:
								print "bomb removed"
								field.piece = self.firstSelected.piece
								self.firstSelected.piece = Piece('', 0)
							else :
								self.firstSelected.piece = Piece('', 0)
						elif field.piece.type == 'F':
							print "Victory!"
							#TODO goto endscreen
						elif field.piece.type == '':
							field.piece = self.firstSelected.piece
							self.firstSelected.piece = Piece('', 0)
						else:
							if field.piece.type < self.firstSelected.piece.type:
								field.piece = self.firstSelected.piece
								self.firstSelected.piece = Piece('', 0)
							elif field.piece.type == self.firstSelected.piece.type:
								self.firstSelected.piece = Piece('', 0)
								field.piece = Piece('',0)
							else:
								self.firstSelected.piece = Piece('', 0)
						
						self.firstSelected = None
					field.selected = False					
				if (field.barrier):
					glColor3f(1, 0, 0)
					
				elif self.firstSelected is field:
					glColor3f(1,0,1)
					
				else:
					glColor3f(1, 1, 1)
				Drawer.drawField(field)
