from godot import exposed, export
from godot import *

global Pause
Pause = False

@exposed
class CanvasLayer(CanvasLayer):
	def _ready(self):
		self.popup = self.get_node("PauseMenu")
		
	def _process(self, delta):
		if Input.is_action_just_pressed("ui_cancel"):
			global Pause
			Pause = not Pause
			
		if Pause is True:
			self.get_tree().paused = True
			self.popup.show()
		else:
			self.get_tree().paused = False
			self.popup.hide()
			
	def _on_ContinueButton_pressed(self):
		global Pause
		Pause = not Pause
		self.get_tree().paused = False
		self.popup.hide()
		
	def _on_SaveButton_pressed(self):
		self.get_tree().change_scene("res://Scenes/Menu.tscn")
		
	def _on_ExitButton_pressed(self):
		self.get_tree().quit()

