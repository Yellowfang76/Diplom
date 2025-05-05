from godot import exposed, export
from godot import *

@exposed
class Player(KinematicBody2D):
	Speed = 200.0
	JumpVelocity = -500.0
	Gravity = 800.0
	JumpSmoothness = 300.0
	MaxJumpTime = 0.2

	def _ready(self):
		self.Up = Vector2(0, -1)
		self.velocity = Vector2()
		self.is_jumping = False
		self.jump_timer = 0.0
		self.animated_sprite = self.get_node("AnimatedSprite")

	def _physics_process(self, delta):
		if Input.is_action_pressed("ui_right"):
			self.velocity.x = self.Speed
			self.animated_sprite.flip_h = False
			self.animated_sprite.play("Run")
		elif Input.is_action_pressed("ui_left"):
			self.velocity.x = -self.Speed
			self.animated_sprite.flip_h = True
			self.animated_sprite.play("Run")
		else:
			self.velocity.x = 0.0
			self.animated_sprite.play("Idle")

		if not self.is_on_floor():
			self.velocity.y += self.Gravity * delta
		else:
			self.velocity.y = 0
			self.is_jumping = False
			self.jump_timer = 0.0

		if self.is_on_floor() and Input.is_action_just_pressed("ui_up"):
			self.velocity.y = self.JumpVelocity
			self.is_jumping = True
			self.jump_timer = 0.0

		if self.is_jumping and Input.is_action_pressed("ui_up"):
			self.jump_timer += delta
			if self.jump_timer < self.MaxJumpTime:
				self.velocity.y -= self.JumpSmoothness * delta
				self.velocity.y = max(self.velocity.y, self.JumpVelocity)

		self.velocity = self.move_and_slide(self.velocity, self.Up)
