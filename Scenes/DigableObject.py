from godot import exposed, export
from godot import *

@exposed
class DigableObject(Area2D):
	def _ready(self):
		if not self.get_node("Timer").is_connected("timeout", self, "_on_Timer_timeout"):
			self.get_node("Timer").connect("timeout", self, "_on_Timer_timeout")

	def start_digging(self):
		self.get_node("Timer").start()

	def _on_Timer_timeout(self):
		self.queue_free()
