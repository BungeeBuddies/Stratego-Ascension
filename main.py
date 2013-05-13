#!/usr/bin/python

import pyglet
from pyglet.gl import *
from math import pi, sin, cos
from time import time
from copy import deepcopy
from field import Field
from piece import Piece
from playscreen import PlayScreen

class Window(pyglet.window.Window):

	def __init__(self):
		super(Window, self).__init__(caption = "Stratego Ascension", config= Config(sample_buffers=1, samples=4))
 		self.set_size(900, 700)
		self.xOffset = 175
		self.yOffset = 75
		self.fieldOffset = 1
		self.firstClick = True

		self.playScreen = PlayScreen(self)
		# self.playScreen.fields = self.createPlayField()
		self.isFieldSelected = False
		self.selectedField = 0

		
		self.amountOfPieces = 80
		self.pieces = self.createPieceList()

	def on_key_press(self, symbol, modifiers):
		pass

	def on_mouse_release(self, x, y, button, modifiers):
		pass

	def on_mouse_press(self, x, y, button, modifiers):
		fieldIndex = 0
		fieldsList = []

		if (self.selectedField is not 0):
			self.selectedField.selected = False

		for row in range(0, len(self.playScreen.fields)):
			for field in self.playScreen.fields[row]:
				fieldsList.append([field.y, field.x])

		fieldSize = self.playScreen.sizeOfField

		for extraX in range(-fieldSize, fieldSize):
			for extraY in range(-fieldSize, fieldSize):
				try:
					fieldIndex = fieldsList.index([y + extraY, x + extraX])
				except ValueError:
					pass
				else:
					index = fieldIndex/self.playScreen.lengthOfField
					self.selectedField = self.playScreen.fields[index][fieldIndex - index*self.playScreen.lengthOfField]
					self.selectedField.selected = True

					if (self.firstClick):
						self.playScreen.color = [1, 0, 1]
						self.firstClick = False
					elif (not self.firstClick):
						self.playScreen.color = [0, 0, 1]						
						self.firstClick = True

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		pass


	def on_mouse_motion(self, x, y, dx, dy):
		pass


	def drawPoint(self, x, y, color):
		pyglet.graphics.draw(1, GL_POINTS,
			('v2i', (x, y)),
			('c3B', (color[0], color[1], color[2])))

	def drawCircle(self, x, y, radius, color):
		smoothness = int(2*radius*pi)
		glBegin(GL_TRIANGLE_FAN)
		glColor3f(color[0], color[1], color[2])
		for i in range(0, smoothness):
			angle = i * pi * 2.0 / smoothness
			glVertex2f(x + radius * cos(angle), y + radius * sin(angle))
		glEnd()

	def createPlayField(self):
		fields = [[Field(0, 0, self.playScreen.sizeOfField) for x in xrange(self.playScreen.lengthOfField)] for y in xrange(self.playScreen.lengthOfField)]

		for y in range(0, len(fields)):
			for x in range(0, len(fields[0])):
					fields[y][x].x = x * fields[y][x].size*2 + self.xOffset + self.fieldOffset * x
					fields[y][x].y = y * fields[y][x].size*2 + self.yOffset + self.fieldOffset * y

		return fields

	def createPieceList(self):
		pieces = []
		#80 pieces, 40 of team a, 40 of team b.
		#So, do everything two times
		for x in range (0,2):
			#Fourty pieces
			#One Flag
			for x in range(0,1):
				pieces.append(Piece('F'))
			#six Bombs
			for x in range(0,6):
				pieces.append(Piece('B'))
			#One Spy
			for x in range(0,1):
				pieces.append(Piece(1))
			#Eight Scouts
			for x in range (0,8):
				pieces.append(Piece(2))
			#Five Miners
			for x in range(0,5):
				pieces.append(Piece(3))	
			#Four Sergeants
			for x in range(0,4):
				pieces.append(Piece(4))
			#Four Lieutenants 
			for x in range(0,4):
				pieces.append(Piece(5))
			#Four Captains
			for x in range(0,4):
				pieces.append(Piece(6))
			#Three Majors
			for x in range(0,3):
				pieces.append(Piece(7))
			#Two Colonels
			for x in range(0,2):
				pieces.append(Piece(8))
			#One General
			for x in range(0,1):
				pieces.append(Piece(9))
			#One Marshal
			for x in range(0,1):
				pieces.append(Piece(10))
		return pieces	
		

	def on_draw(self):
		pass

	def update(self, dt):
		self.playScreen.draw()

if __name__ == '__main__':
	window = Window()
	pyglet.clock.schedule_interval(window.update, 1.0/60.0)
	pyglet.app.run()
