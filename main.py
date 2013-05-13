#!/usr/bin/python

import pyglet
from pyglet.gl import *
from math import pi, sin, cos
from time import time
from copy import deepcopy
from field import Field

class Window(pyglet.window.Window):

	def __init__(self):
		super(Window, self).__init__()
		self.set_size(800, 600)
		self.lengthOfField = 10
		self.sizeOfField = 50
		self.xOffset = 175
		self.yOffset = 100

		self.fields = self.createPlayField()

	def on_key_press(self, symbol, modifiers):
		pass

	def on_mouse_release(self, x, y, button, modifiers):
		pass

	def on_mouse_press(self, x, y, button, modifiers):
		fieldIndex = 0
		fieldsList = []
		print [y, x]

		for row in range(0, len(self.fields)):
			for field in self.fields[row]:
				fieldsList.append([field.y, field.x])

		fieldSize = self.sizeOfField/2

		for extraX in range(-fieldSize, fieldSize):
			for extraY in range(-fieldSize, fieldSize):
				try:
					fieldIndex = fieldsList.index([y + extraY, x + extraX])
				except ValueError:
					pass
				else:
					print "Field pressed: " + str(fieldIndex)

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
		fields = [[Field(0, 0, self.sizeOfField) for x in xrange(self.lengthOfField)] for y in xrange(self.lengthOfField)]

		for y in range(0, len(fields)):
			for x in range(0, len(fields[0])):
				fields[y][x].x = x * fields[y][x].size + self.xOffset
				fields[y][x].y = y * fields[y][x].size + self.yOffset

		return fields

	def drawPlayField(self):
		for y in range(0, len(self.fields)):
			for field in self.fields[y]:

				# Draw center
				self.drawCircle(field.x, field.y, 5, [1, 1, 1])

				# Draw top side
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
		

	def on_draw(self):
		pass

	def update(self, dt):
		self.drawPlayField()

if __name__ == '__main__':
	window = Window()
	pyglet.clock.schedule_interval(window.update, 1.0/60.0)
	pyglet.app.run()
