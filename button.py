from piece import Piece
import pyglet
class Button(object):

	def __init__(self, x, y, xSize, ySize):
		self._x = x
		self._y = y
		self.xSize = xSize
		self.ySize = ySize
		self.selected = False
		self.hover = False
		self.label = pyglet.text.HTMLLabel("",
                          x=self._x, y=self._y,
                          multiline = True,
                          width = 50,
                          anchor_x='center', anchor_y='center')

	def x():
	    doc = "The x property."
	    def fget(self):
	        return self._x
	    def fset(self, value):
	        self._x = value
	        self.label.x = value
	    def fdel(self):
	        del self._x
	    return locals()
	x = property(**x())

	def y():
	    doc = "The y property."
	    def fget(self):
	        return self._y
	    def fset(self, value):
	        self._y = value
	        self.label.y = value

	    def fdel(self):
	        del self._y
	    return locals()
	y = property(**y())
