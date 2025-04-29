from godot import exposed, export
from godot import *

@exposed
class Player(KinematicBody2D):
	# Определяем константы
	Speed = 200.0
	JumpVelocity = -500.0  # Максимальная скорость прыжка
	Gravity = 800.0        # Гравитация (ускорение свободного падения)
	JumpSmoothness = 1000.0  # Скорость изменения скорости при прыжке
	DigRadius = 100.0      # Радиус копания

	def _ready(self):
		# Направление "вверх"
		self.Up = Vector2(0, -1)
		self.velocity = Vector2()  # Текущая скорость персонажа
		self.is_jumping = False    # Флаг для отслеживания состояния прыжка

	def _physics_process(self, delta):
		# Управление движением по горизонтали
		if Input.is_action_pressed("ui_right"):
			self.velocity.x = self.Speed
		elif Input.is_action_pressed("ui_left"):
			self.velocity.x = -self.Speed
		else:
			self.velocity.x = 0.0

		# Добавляем гравитацию (если не на земле)
		if not self.is_on_floor():
			self.velocity.y += self.Gravity * delta
			self.is_jumping = True  # Персонаж находится в воздухе
		else:
			self.velocity.y = 0
			self.is_jumping = False  # Персонаж на земле

		# Проверяем, находится ли персонаж на земле, и обрабатываем прыжок
		if self.is_on_floor() and Input.is_action_just_pressed("ui_up"):
			# Начинаем плавный прыжок
			self.velocity.y = 0  # Обнуляем вертикальную скорость перед прыжком
			self.is_jumping = True

		# Если игрок продолжает удерживать клавишу прыжка, увеличиваем скорость
		if self.is_jumping and Input.is_action_pressed("ui_up"):
			self.velocity.y -= self.JumpSmoothness * delta
			# Ограничиваем максимальную скорость прыжка
			self.velocity.y = max(self.velocity.y, self.JumpVelocity)

		# Применяем движение с учетом направления "вверх"
		self.velocity = self.move_and_slide(self.velocity, self.Up)

		# Обработка копания
		self.handle_digging()

	def handle_digging(self):
		# Проверяем нажатие левой кнопки мыши
		if Input.is_action_just_pressed("ui_select"):
			# Получаем позицию курсора
			mouse_position = get_viewport().get_mouse_position()
			world_position = self.get_global_mouse_position()

			# Находим объекты в радиусе копания
			objects_in_range = self.get_objects_in_dig_radius(world_position)

			# Если найден объект под курсором
			for obj in objects_in_range:
				if obj.has_method("on_dug"):
					obj.on_dug()
					break

	def get_global_mouse_position(self):
		# Преобразуем позицию курсора в мировые координаты
		viewport = self.get_viewport()
		mouse_pos = viewport.get_mouse_position()
		camera = self.get_viewport().get_camera()
		return camera.get_global_transform().affine_inverse().xform(mouse_pos)

	def get_objects_in_dig_radius(self, position):
		# Находим все объекты в радиусе копания
		objects = []
		for body in self.get_world_2d().direct_space_state.intersect_point(
			position, self.DigRadius
		):
			if body.collider.has_method("on_dug"):
				objects.append(body.collider)
		return objects
