import pyglet
import copy
from pyglet.gl import *
from field import Field
from piece import Piece
from drawer import Drawer
import threading
from threading import Lock

class PlayScreen:

	def __init__(self, window):
		self.window = window
		self.width = 900
		self.height = 700
		self.xOffset = self.width/4
		self.yOffset = self.height/8 + 35
		self.fieldOffset = 1
		self.barrierFields = [[2, 4], [3, 4], [6, 4], [7, 4], [2, 5], [3, 5], [6, 5], [7, 5]]
		
		self.playersTurn = 2
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
		self.visibleEnemy = None
		self.lockDownTime = 0.5
		self.lockDown = False
		self.headerP2 = pyglet.text.Label("Player 2's turn!",
                          font_name='Arial',
                          font_size=16,
                          color=(0,0,255,255),
                          x=self.window.get_size()[0]/2, y=self.window.get_size()[1]-20,
                          anchor_x='center', anchor_y='center')
		self.headerP1 = pyglet.text.Label("Player 1's turn!",
	                      color=(255,0,0,255),
                          font_name='Arial',
                          font_size=16,
                          x=self.window.get_size()[0]/2, y=self.window.get_size()[1]-20,
                          anchor_x='center', anchor_y='center')
		self.changePlayerTurn();
		self.hiddenField = Field(0,0,0)
		self.hiddenField.piece = Piece('?',0)
		
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
		if self.playersTurn == 1:
			self.headerP1.draw()
		else:
			self.headerP2.draw()
		# Draw fields
		for y in range(0, len(self.fields)):
			for x in range( 0,len(self.fields[y])):	
				field = self.fields[y][x]			
				if field.selected and self.lockDown == False:				
					if self.firstSelected is None:
						if field.piece.type != '' and field.piece.type is not 'F' and field.piece.type is not'B' and field.piece.type is not '#' and field.piece.owner == self.playersTurn:
								self.firstSelected = field
								self.firstSelectedXPosition = x
								self.firstSelectedYPosition = y
					elif self.firstSelected is field:
						self.firstSelected = None
					elif field.piece.type != '#':
						if self.legalMove(self.firstSelected,self.firstSelectedXPosition,self.firstSelectedYPosition,field,x,y) and self.firstSelected.piece.owner != field.piece.owner:
							if field.piece.type == '':
								field.piece = self.firstSelected.piece
								self.firstSelected.piece = Piece('', 0)
								self.changePlayerTurn()
							else:
								self.visibleEnemy = field
								self.lockDown = True
								self.textResetTimer = threading.Timer(self.lockDownTime,self.onLockDownFinish)
								self.textResetTimer.start()
					field.selected = False
				if field.piece.owner != self.playersTurn and field.piece.owner != 0 and field is not self.visibleEnemy:
					self.hiddenField.x = field.x
					self.hiddenField.y = field.y
					self.hiddenField.size = field.size
					self.hiddenField.piece.owner = field.piece.owner
					field = self.hiddenField
				if self.firstSelected is field:			
					glColor3f(1, 0, 1)
				elif field.piece.owner == 2:
					glColor3f(0, 0, 1)
				elif field.piece.owner == 1:
					glColor3f(1, 0, 0)
				else:
					glColor3f(1, 1, 1)
				Drawer.drawField(field)

	def legalMove(self, source,sourceX,sourceY,target,targetX,targetY):
		if sourceX == targetX or sourceY == targetY: #both fields are on the same line
			delta = ( sourceY - targetY if sourceX == targetX  else sourceX - targetX) #the difference between the fields
			if abs(delta) <= source.piece.steps: #check if the piece can move this far
				if source.piece.steps > 1:
					if sourceX == targetX:	#finally: check if something is in between (only applies if piece can set more then one step)
						step = -1 if sourceY > targetY else 1 
						for y in xrange(sourceY+step,targetY,step):
							if self.fields[y][sourceX].piece.type != '':
								return False
					else:
						step = -1 if sourceX > targetX else 1
						for x in xrange(sourceX+step,targetX,step):
							if self.fields[sourceY][x].piece.type != '':
								return False
				return True
		return False

	def onLockDownFinish(self):
		field = self.visibleEnemy		
		if field.piece.type == 10:
			if self.firstSelected.piece.type == 1:
				field.piece = self.firstSelected.piece
				self.firstSelected.piece = Piece('', 0)
			else:
				self.firstSelected.piece = Piece('',0)
		elif field.piece.type == 'B':
			if self.firstSelected.piece.type == 3:
				field.piece = self.firstSelected.piece
				self.firstSelected.piece = Piece('', 0)
			else :
				self.firstSelected.piece = Piece('', 0)
		elif field.piece.type == 'F':
			print "Victory!"
			self.window.currentScreen = self.window.victoryScreen
			#TODO goto endscreen
		else:
			if field.piece.type < self.firstSelected.piece.type:
				field.piece = self.firstSelected.piece
				self.firstSelected.piece = Piece('', 0)
			elif field.piece.type == self.firstSelected.piece.type:
				self.firstSelected.piece = Piece('', 0)
				field.piece = Piece('',0)
			else:
				self.firstSelected.piece = Piece('', 0)
		self.changePlayerTurn()
		self.lockDown = False	

	def changePlayerTurn(self):
		self.firstSelected = None
		self.visibleEnemy = None
		if self.playersTurn == 1:
			self.playersTurn = 2
		else:
			self.playersTurn = 1