from godot import exposed, Node2D

@exposed
class Tile(Node2D):
	def _ready(self):
		self.animated_sprite = self.get_node("AnimatedSprite")
		self.static_body = self.get_node("StaticBody2D")

	def _on_Button_pressed(self):
		self.animated_sprite.play("Mining")

	def _on_animation_finished(self):
		self.queue_free()
