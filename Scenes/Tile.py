from godot import exposed, Node2D
global DMG
DMG = 0.5

@exposed
class Tile(Node2D):
	def _ready(self):
		self.animated_sprite = self.get_node("AnimatedSprite")
		self.static_body = self.get_node("StaticBody2D")
		self.HP = 5

	def _on_Button_pressed(self):
		if self.HP > 0:
			self.animated_sprite.play("Mining")

	def _on_animation_finished(self):
		self.HP -= DMG
		if self.HP <= 0:
			self.queue_free()
		else:
			self.animated_sprite.play("Idle")
