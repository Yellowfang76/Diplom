from godot import exposed, export
from godot import *

@exposed
class Player(KinematicBody2D):
	# Константы
	Speed = 200.0
	JumpVelocity = -500.0
	Gravity = 800.0
	JumpSmoothness = 1000.0
	MaxJumpTime = 0.2  # Максимальное время усиления прыжка (в секундах)
	FlightBoost = -300.0  # Дополнительная скорость полёта при нажатии Shift

	def _ready(self):
		self.Up = Vector2(0, -1)
		self.velocity = Vector2()
		self.is_jumping = False
		self.jump_timer = 0.0  # Таймер для отслеживания времени усиления прыжка
		# Получаем доступ к AnimatedSprite
		self.animated_sprite = self.get_node("AnimatedSprite")

	def _physics_process(self, delta):
		# Управление движением по горизонтали
		if Input.is_action_pressed("ui_right"):
			self.velocity.x = self.Speed
			self.animated_sprite.flip_h = False  # Не отражаем спрайт
			self.animated_sprite.play("Run")  # Воспроизводим анимацию бега
		elif Input.is_action_pressed("ui_left"):
			self.velocity.x = -self.Speed
			self.animated_sprite.flip_h = True  # Отражаем спрайт по горизонтали
			self.animated_sprite.play("Run")  # Воспроизводим анимацию бега
		else:
			self.velocity.x = 0.0
			self.animated_sprite.play("Idle")  # Воспроизводим анимацию покоя

		# Гравитация
		if not self.is_on_floor():
			self.velocity.y += self.Gravity * delta
			self.is_jumping = True
		else:
			self.velocity.y = 0
			self.is_jumping = False
			self.jump_timer = 0.0  # Сбрасываем таймер при приземлении

		# Прыжок
		if self.is_on_floor() and Input.is_action_just_pressed("ui_up"):
			self.velocity.y = self.JumpVelocity  # Начинаем прыжок
			self.is_jumping = True
			self.jump_timer = 0.0  # Сбрасываем таймер

		# Усиление прыжка
		if self.is_jumping and Input.is_action_pressed("ui_up"):
			self.jump_timer += delta  # Увеличиваем таймер
			if self.jump_timer < self.MaxJumpTime:
				# Усиливаем прыжок, если таймер не превышен
				self.velocity.y -= self.JumpSmoothness * delta
				self.velocity.y = max(self.velocity.y, self.JumpVelocity)

		# Полёт с Shift
		if self.is_jumping and Input.is_action_pressed("ui_shift"):
			self.velocity.y += self.FlightBoost * delta  # Добавляем дополнительную силу полёта

		# Перемещение персонажа
		self.velocity = self.move_and_slide(self.velocity, self.Up)
