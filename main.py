#!/usr/bin/python

import pyglet
from pyglet.gl import *
from math import pi, sin, cos
from time import time
from copy import deepcopy

class Window(pyglet.window.Window):

	def __init__(self):
		super(Window, self).__init__()
		self.set_size(800, 600)

	def on_key_press(self, symbol, modifiers):
		pass

	def on_mouse_release(self, x, y, button, modifiers):
		pass

	def on_mouse_press(self, x, y, button, modifiers):
		pass
					
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		pass


	def on_mouse_motion(self, x, y, dx, dy):
		pass


	def drawPoint(self, x, y, color):
		pyglet.graphics.draw(1, GL_POINTS,
			('v2i', (x, y)),
			('c3B', (color[0], color[1], color[2])))

	def circle(self, x, y, radius, color):
		smoothness = int(2*radius*pi)
		glBegin(GL_TRIANGLE_FAN)
		glColor3f(color[0], color[1], color[2])
		for i in range(0, smoothness):
			angle = i * pi * 2.0 / smoothness
			glVertex2f(x + radius * cos(angle), y + radius * sin(angle))
			glEnd()

	def on_draw(self):
		pass

	def update(self, dt):
		pass

if __name__ == '__main__':
	window = Window()
	pyglet.clock.schedule_interval(window.update, 1.0/60.0)
	pyglet.app.run()
