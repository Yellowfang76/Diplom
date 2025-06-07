from godot import exposed, export, Node2D, Timer, Vector2, Input, ResourceLoader

global Coin
Coin = 0
save_path = "res://save/Save/save.save"  # Фиксируем имя файла

@exposed
class Game(Node2D):
	def _ready(self):
		self.popup = self.get_node("CanvasLayer")
		self.money_label = self.popup.get_node("MoneyLabel")
		self.player = self.get_node("Player")  # Предположим, что игрок называется "Player"
		Money = 'MONEY: ' + str(Coin)
		self.money_label.set_text(Money)
		
		self.spawn_tiles()

		# Создаем таймер для восстановления области
		self.restore_timer = Timer.new()
		self.restore_timer.set_wait_time(300)  # 5 минут = 300 секунд
		self.restore_timer.set_one_shot(False)
		self.restore_timer.connect("timeout", self, "_on_restore_timer_timeout")
		self.add_child(self.restore_timer)
		self.restore_timer.start()

	def spawn_tiles(self):
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

		tiles_container = self.get_node("TilesContainer")
		if not tiles_container:
			print("Контейнер для тайлов не найден!")
			return

		for child in tiles_container.get_children():
			child.queue_free()

		total_columns = ((end_x - start_x) // tile_size) + 1

		row_index = 0
		y = start_y
		while y <= end_y:
			level = row_index
			trim_sides = level // 3

			new_start_x = start_x + trim_sides * tile_size
			new_end_x = end_x - trim_sides * tile_size

			x = new_start_x
			while x <= new_end_x:
				tile = tile_scene.instance()
				tile.position = Vector2(x, y)
				tiles_container.add_child(tile)
				x += tile_size
	
			y += tile_size
			row_index += 1

	def _on_restore_timer_timeout(self):
		# Проверяем, находится ли игрок внутри области копания
		player_pos = self.player.position
		if self.is_player_in_mine_area(player_pos):
			# Телепортируем игрока на заданные координаты
			self.player.position = Vector2(-520, -304)

		# Восстанавливаем область копания
		self.spawn_tiles()

	def is_player_in_mine_area(self, pos):
		# Задаем границы области копания
		min_x = 96
		max_x = 480
		min_y = 320
		max_y = 512

		return min_x <= pos.x <= max_x and min_y <= pos.y <= max_y

	def _on_MineGuideButton_pressed(self):
		guide = self.get_node("MineGuideButton")
		guide.hide()
			
	def _on_UpgradeGuideButton_pressed(self):
		guide = self.get_node("UpgradeGuideButton")
		guide.hide()

	def _process(self, delta):
		if Input.is_action_just_pressed("ui_shift"):
			global Coin
			Coin += 1
			Money = 'MONEY: ' + str(Coin)
			self.money_label.set_text(Money)
