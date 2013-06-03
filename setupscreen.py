#Defines the playfield and then passes it on to the playscreen
import pyglet
import copy
import threading
import random

from pyglet.gl import *
from field import Field
from piece import Piece
from button import Button
from drawer import Drawer

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
		self.fields = self.createStartField()
		self.extraFields = self.setupExtraFields()

		self.buttonXSize = 50
		self.buttonYSize = 25

		self.buttons = self.createButtons()

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
		return fields

	def createButtons(self):
		amountOfButtons = 2
		buttons = [Button(0, 0, self.buttonXSize,self.buttonYSize) for x in xrange(amountOfButtons)]
		buttons[0].label.text = "Done!"
		buttons[0].x = self.window.get_size()[0]/8
		buttons[0].y = self.window.get_size()[1]/4
		buttons[1].label.text = "Autofill"
		buttons[1].x = self.window.get_size()[0]/8*7
		buttons[1].y = self.window.get_size()[1]/4
		return buttons

	def setupExtraFields(self):
		fields = [Field(0, 0, self.sizeOfField) for x in xrange(self.widthOfField)]

		for n in range(0, len(fields)):
			fields[n].x = n * fields[n].size*2 + self.xOffset + self.fieldOffset * n
			fields[n].y = len(self.fields) * fields[n].size*2 + self.yOffset + self.extraYOffset  + self.fieldOffset * len(self.fields)
		return fields


	def populateField(self):
		for y in range(len(self.fields)/2,len(self.fields)):
			for x in range(0,len(self.fields[y])):
				self.fields[y][x].piece = Piece('', 0)
		for y in range(0,len(self.fields)/2):
			for x in range(0,len(self.fields[y])):
				self.fields[y][x].piece = self.pieces[y*10+x]
		self.extraFields[2].piece = self.extraFields[3].piece = self.extraFields[6].piece = self.extraFields[7].piece = Piece('#',0) 

	def draw(self):
		self.header.draw()
		self.footer.draw()
		for y in range(0, len(self.fields)):
			for field in self.fields[y]:
				
				if field.selected:
					
					if self.firstSelected is None:
						
						if field.piece.type != '':
							self.firstSelected = field
					else: 
						
						if field.piece.type == '':
							field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
							self.firstSelected.piece = Piece('', 0)
						else:
							if field.piece.type != self.firstSelected.piece.type:
								helpPiece = self.firstSelected.piece
								self.firstSelected.piece = field.piece
								field.piece = helpPiece
						self.firstSelected = None

				field.selected = False
				
				if field is self.firstSelected:
					glColor3f(1, 0, 1)
				else:
					glColor3f(1, 1, 1)
				Drawer.drawField(field)

		for field in self.extraFields:
			glColor3f(1, 0, 0)
			Drawer.drawField(field)

		glColor3f(1, 1, 1)
		if self.buttons[0].selected:
			# self.buttons[0].selected = False
			if  not self.checkIfDone():
				self.footer.text = "You have to place all your pieces before you can continue"
				if hasattr(self, 'textResetTimer') and self.textResetTimer.isAlive():
					self.textResetTimer.cancel()
					self.textResetTimer.join()
				self.textResetTimer = threading.Timer(3,self.resetBottomText)
				self.textResetTimer.start()
		if self.buttons[1].selected:
			self.autofill()
			# self.buttons[1].selected = False
		for button in self.buttons:
			Drawer.drawButton(button)

	def checkIfDone(self):
		for y in range(0,len(self.fields)/2):
			for x in range(0,len(self.fields[y])):
				if self.fields[y][x].piece.type != '':
					return False
		self.activePlayer += 1
		self.resetBottomText(); 
		if self.activePlayer == 2:
			for y in xrange(len(self.fields)/2,len(self.fields)):
				for x in xrange(0,len(self.fields[y])):
					self.window.playScreen.fields[len(self.window.playScreen.fields) + len(self.fields)/2 - y - 1][len(self.fields[y])-x-1].piece = self.fields[y][x].piece
					self.window.playScreen.player1Pieces.append(self.fields[y][x].piece)		
		else: 
			for y in xrange(len(self.fields)/2,len(self.fields)):
				for x in xrange(0,len(self.fields[y])):
					self.window.playScreen.fields[-len(self.fields)/2 + y][x].piece = self.fields[y][x].piece
					self.window.currentScreen = self.window.playScreen
					self.window.playScreen.player2Pieces.append(self.fields[y][x].piece)
		self.populateField()
		return True			

	def resetBottomText(self):
		self.footer.text = 'Player ' + str(self.activePlayer) + ', setup your field'

	def autofill(self):
		self.firstSelected = None
		regels = self.fields[:len(self.fields)/2] 
		emptyfields = [f for r in regels for f in r if f.piece.type != '']
		topping = self.fields[len(self.fields)/2:] 
		tobefilledfields = [f for r in topping for f in r if f.piece.type == '']
		random.shuffle(tobefilledfields)
		for (a, b) in zip(emptyfields, tobefilledfields):
			b.piece = a.piece
			a.piece = Piece('', 0)
			
			
			
			