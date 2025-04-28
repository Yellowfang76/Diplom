from godot import exposed, export
from godot import *

@exposed
class LoadSave(Node2D):
	def _on_BackButton_pressed(self):
		self.get_tree().change_scene("res://Menu.tscn")
