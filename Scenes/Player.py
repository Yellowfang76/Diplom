from godot import exposed, export
from godot import *

@exposed
class Player(KinematicBody2D):
	Speed = 200.0
	JumpVelocity = -300.0
	Gravity = 800.0
	JumpSmoothness = 300.0
	MaxJumpTime = 0.1

	def _ready(self):
		self.Up = Vector2(0, -1)
		self.velocity = Vector2()
		self.is_jumping = False
		self.jump_timer = 0.0
		self.mining = False
		self.animated_sprite = self.get_node("AnimatedSprite")
		self.rays = {
			"left": self.get_node("RayCast2DLeft"),
			"right": self.get_node("RayCast2DRight"),
			"up": self.get_node("RayCast2DUp"),
			"down": self.get_node("RayCast2DDown"),
		}

	def _physics_process(self, delta):
		if self.mining:
			# Если в процессе копания, не двигаем персонажа
			self.velocity.x = 0.0
			if Input.is_action_just_released("ui_LMB"):
				self.mining = False
				# Возвращаем Idle или Run, в зависимости от движения
				if self.velocity.x == 0:
					self.animated_sprite.play("Idle")
				else:
					self.animated_sprite.play("Run")
			return

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

		# ������ Проверка нажатия ЛКМ и направления клика
		if Input.is_action_just_pressed("ui_LMB"):
			mouse_pos = self.get_global_mouse_position()
			player_pos = self.global_position

			# Определяем сторону клика
			if mouse_pos.x < player_pos.x:
				# Клик слева → отразить спрайт
				self.animated_sprite.flip_h = True
			else:
				# Клик справа → не отражать
				self.animated_sprite.flip_h = False

			self.animated_sprite.play("Mine")
			self.mining = True  # Включаем режим копания

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
