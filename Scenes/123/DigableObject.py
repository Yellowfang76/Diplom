from godot import exposed, export
from godot import *
from godot import exposed, Node2D

@exposed
class Tile(Node2D):
	def dig(self):
		self.queue_free()
