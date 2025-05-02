from godot import exposed, export
from godot import *

@exposed
class DigableObject(Area2D):
	def _ready(self):
		# Подключаем сигнал таймера
		if not self.get_node("Timer").is_connected("timeout", self, "_on_Timer_timeout"):
			self.get_node("Timer").connect("timeout", self, "_on_Timer_timeout")

	def start_digging(self):
		# Запускаем таймер для анимации разрушения
		self.get_node("Timer").start()

	def _on_Timer_timeout(self):
		# Удаляем объект после завершения таймера
		self.queue_free()
