from godot import exposed, export
from godot import *

global save_name
save_name = ""

@exposed
class Menu(Node2D):

	def _ready(self):
		self.popup = self.get_node("Panel")

	def _on_LoadButton_pressed(self):
		self.popup.show()

	def _on_BackButton_pressed(self):
		self.popup.hide()

	def _on_LoadSave1Button_pressed(self):
		self.get_tree().change_scene("res://Scenes/Game.tscn")
		save_name = "Save1"

	def _on_LoadSave2Button_pressed(self):
		self.get_tree().change_scene("res://Scenes/Game.tscn")
		save_name = "Save2"

	def _on_LoadSave3Button_pressed(self):
		self.get_tree().change_scene("res://Scenes/Game.tscn")
		save_name = "Save3"

	def _on_ExitButton_pressed(self):
		self.get_tree().quit()
