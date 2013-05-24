from piece import Piece
import pyglet
class Button(object):

	def __init__(self, x, y, xSize, ySize):
		self._x = x
		self._y = y
		self.xSize = xSize
		self.ySize = ySize
		self.selected = False
		self._piece = Piece('')
		self.label = pyglet.text.Label(self._piece.type,
                          font_name='Arial',
                          font_size=16,
                          x=self._x, y=self._y,
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

	def piece():
	    doc = "The piece property."
	    def fget(self):
	        return self._piece
	    def fset(self, value):
	        self._piece = value
	        self.label.text = str(value.type)

	    def fdel(self):
	        del self._piece
	    return locals()
	piece = property(**piece())
