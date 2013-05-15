from piece import Piece
import pyglet
class Field:

	def __init__(self, x, y, size):
		self.x = x
		self.y = y
		self.size = size
		self.selected = False
		self.piece = Piece('')