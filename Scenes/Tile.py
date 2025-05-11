from godot import exposed, export, Node2D
from godot import *
from godot import exposed, Node2D

@exposed
class Tile(Node2D):
	def dig(self):
		print(f"Tile at {self.position} is being dug!")
		self.queue_free()
