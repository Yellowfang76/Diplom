from godot import exposed, export
from godot import *

@exposed
class DiggableObject(Area2D):
	def _ready(self):
		# Подключаем сигнал входа в область
		self.connect("body_entered", self.on_body_entered)

	def on_dug(self):
		# Уничтожаем объект при копании
		self.queue_free()

	def on_body_entered(self, body):
		# Проверяем, что вошедший объект — это игрок
		if isinstance(body, Player):
			print(f"Player entered the diggable area of {self.name}")
