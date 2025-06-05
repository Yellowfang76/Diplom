from godot import exposed, export
from godot import *
import json

global Coin
Coin = 0
save = ""
save_path = "res://save/Save/" + str(save) + ".save"

@exposed
class Game(Node2D):
	def _ready(self):
		self.popup = self.get_node("CanvasLayer")
		self.money_label = self.popup.get_node("MoneyLabel")
		Money = 'MONEY: ' + str(Coin)
		self.money_label.set_text(Money)

		# Загрузка тайлов
		self.spawn_tiles()

	def spawn_tiles(self):
		# Параметры области генерации
		start_x = 104
		start_y = 328
		end_x = 472
		end_y = 504
		tile_size = 16
	
		scene_path = "res://Scenes/Tile.tscn"
		tile_scene = ResourceLoader.load(scene_path)
	
		if not tile_scene:
			print("Ошибка загрузки сцены:", scene_path)
			return
	
		# Получаем контейнер для тайлов
		tiles_container = self.get_node("TilesContainer")  # <- должен существовать в сцене
		if not tiles_container:
			print("Контейнер для тайлов не найден!")
			return
	
		# Очищаем предыдущие тайлы (если нужно)
		for child in tiles_container.get_children():
			child.queue_free()
	
		# Вычисляем количество колонок изначально
		total_columns = ((end_x - start_x) // tile_size) + 1
	
		# Генерация сетки тайлов
		row_index = 0  # Номер уровня (строки) от верхней границы
		y = start_y
		while y <= end_y:
			level = row_index  # текущий уровень (глубина)
			trim_sides = level // 3  # сколько тайлов убрать с каждой стороны на этом уровне
	
			# Вычисляем новые границы X с учётом обрезания
			new_start_x = start_x + trim_sides * tile_size
			new_end_x = end_x - trim_sides * tile_size
	
			# Пробегаем по X в пределах новых границ
			x = new_start_x
			while x <= new_end_x:
				tile = tile_scene.instance()
				tile.position = Vector2(x, y)
				tiles_container.add_child(tile)
				x += tile_size
	
			y += tile_size
			row_index += 1

	def _process(self, delta):
		if Input.is_action_just_pressed("ui_shift"):
			global Coin
			Coin += 1
			Money = 'MONEY: ' + str(Coin)
			self.money_label.set_text(Money)
			self.spawn_tiles()
