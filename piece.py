class Piece:
	# the #-symbol makes a blokkade
	def __init__(self,type,steps):
		self.type = type
		self.owner = 0
		self.steps = steps
