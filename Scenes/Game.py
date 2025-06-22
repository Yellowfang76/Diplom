from godot import exposed, Node2D, Timer, ResourceLoader, Vector2
import json, os

global Pause
Pause = False
SAVE_DIR = "save"
CURRENT_SAVE_FILE = f"{SAVE_DIR}/CurrentSaveDir.json"

@exposed
class Game(Node2D):
	def _ready(self):
		self.current_save_path = self._get_current_save_file()
		print(f"[Загрузка] Используется сохранение: {self.current_save_path}")

		os.makedirs(SAVE_DIR, exist_ok=True)

		self.data = self._load_data()

		self.popup = self.get_node("CanvasLayer")
		self.money_label = self.popup.get_node("MoneyLabel")
		self.dmg_label = self.popup.get_node("DMGLabel")
		
		self.UpdateMenuCanvasLayer = self.get_node("UpdateMenuCanvasLayer")
		self.UpdateMenu = self.UpdateMenuCanvasLayer.get_node("UpdateMenu")

		self._update_money_label()
		self._update_dmg_label()
		self._update_dmg_cost_label()

		self.save_check_timer = Timer.new()
		self.save_check_timer.set_wait_time(0.5)
		self.save_check_timer.set_one_shot(False)
		self.save_check_timer.connect("timeout", self, "_check_save_file")
		self.add_child(self.save_check_timer)
		self.save_check_timer.start()

		self.spawn_tiles()

		self.restore_timer = Timer.new()
		self.restore_timer.set_wait_time(300)
		self.restore_timer.set_one_shot(False)
		self.restore_timer.connect("timeout", self, "_on_restore_timer_timeout")
		self.add_child(self.restore_timer)
		self.restore_timer.start()

	def _get_current_save_file(self):
		try:
			if not os.path.exists(CURRENT_SAVE_FILE):
				return f"{SAVE_DIR}/Save1.json"

			with open(CURRENT_SAVE_FILE, "r") as f:
				data = json.load(f)
				return data.get("current_save", f"{SAVE_DIR}/Save1.json")
		except Exception as e:
			print(f"[Ошибка] Не удалось прочитать CurrentSaveDir.json: {e}")
			return f"{SAVE_DIR}/Save1.json"

	def _load_data(self):
		if not os.path.exists(self.current_save_path):
			# ✅ Добавляем все необходимые поля
			default_data = {
				"Coin": 0,
				"DMG": 1,
				"DMGUpgradeCost": 10,
				"BrokenBlocks": 0,
				"HPBonus": 0
			}
			self._save_data(default_data)
			return default_data
	
		with open(self.current_save_path, "r") as f:
			content = f.read().strip()
			if not content:
				default_data = {
					"Coin": 0,
					"DMG": 1,
					"DMGUpgradeCost": 10,
					"BrokenBlocks": 0,
					"HPBonus": 0
				}
				self._save_data(default_data)
				return default_data
	
			try:
				data = json.loads(content)
				# ✅ Устанавливаем значения по умолчанию для всех полей
				data.setdefault("Coin", 0)
				data.setdefault("DMG", 1)
				data.setdefault("DMGUpgradeCost", 10)
				data.setdefault("BrokenBlocks", 0)
				data.setdefault("HPBonus", 0)
				return data
			except json.JSONDecodeError:
				print(f"[Ошибка] JSON повреждён в {self.current_save_path}, создаём дефолтные данные...")
				default_data = {
					"Coin": 0,
					"DMG": 1,
					"DMGUpgradeCost": 10,
					"BrokenBlocks": 0,
					"HPBonus": 0
				}
				self._save_data(default_data)
				return default_data

	def _save_data(self, data=None):
		if data is None:
			data = self.data
	
		# ✅ Гарантируем наличие всех полей перед записью
		data.setdefault("Coin", 0)
		data.setdefault("DMG", 1)
		data.setdefault("DMGUpgradeCost", 10)
		data.setdefault("BrokenBlocks", 0)
		data.setdefault("HPBonus", 0)
	
		with open(self.current_save_path, "w") as f:
			json.dump(data, f, indent=4)
		print(f"[Сохранение] Данные записаны в {self.current_save_path}")

	def _update_money_label(self):
		self.money_label.set_text(f"MONEY: {self.data['Coin']}")

	def _update_dmg_label(self):
		self.dmg_label.set_text(f"DMG: {self.data['DMG']}")

	def update_money(self):
		self.data["Coin"] += 1
		self._save_data()
		self._update_money_label()
		self._update_dmg_label()

	def _check_save_file(self):
		with open(self.current_save_path, "r") as f:
			content = f.read().strip()
			if not content:
				return
	
			try:
				new_data = json.loads(content)
			except json.JSONDecodeError:
				return
	
			# ✅ Добавляем новые поля в проверку
			new_data.setdefault("Coin", 0)
			new_data.setdefault("DMG", 1)
			new_data.setdefault("DMGUpgradeCost", 10)
			new_data.setdefault("BrokenBlocks", 0)
			new_data.setdefault("HPBonus", 0)
	
			if (new_data.get("Coin") != self.data.get("Coin") or
				new_data.get("DMG") != self.data.get("DMG") or
				new_data.get("DMGUpgradeCost") != self.data.get("DMGUpgradeCost") or
				new_data.get("BrokenBlocks") != self.data.get("BrokenBlocks") or
				new_data.get("HPBonus") != self.data.get("HPBonus")):
	
				self.data["Coin"] = new_data.get("Coin", self.data["Coin"])
				self.data["DMG"] = new_data.get("DMG", self.data["DMG"])
				self.data["DMGUpgradeCost"] = new_data.get("DMGUpgradeCost", self.data["DMGUpgradeCost"])
				self.data["BrokenBlocks"] = new_data.get("BrokenBlocks", self.data["BrokenBlocks"])
				self.data["HPBonus"] = new_data.get("HPBonus", self.data["HPBonus"])
	
				self._update_money_label()
				self._update_dmg_label()
				self._update_dmg_cost_label()
	
				print("Обнаружено изменение в сохранении. Все данные обновлены.")

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
		player = self.get_node("Player")
		if player is None:
			print("Ошибка: Игрок не найден!")
			return
	
		player_pos = player.position
		if self.is_player_in_mine_area(player_pos):
			player.position = Vector2(player_pos.x, 304)
		self.spawn_tiles()

	def is_player_in_mine_area(self, pos):
		min_x = 96
		max_x = 480
		min_y = 320
		max_y = 512
		return min_x <= pos.x <= max_x and min_y <= pos.y <= max_y

	def set_pause_state(self, paused):
		self.set_process(not paused)
		self.set_physics_process(not paused)
		for child in self.get_children():
			if hasattr(child, "set_process"):
				child.set_process(not paused)
			if hasattr(child, "set_physics_process"):
				child.set_physics_process(not paused)

	def _update_dmg_cost_label(self):
		self.UpdateDMGButton = self.UpdateMenu.get_node("UpdateDMGButton")
		self.DMGCostLabel = self.UpdateDMGButton.get_node("DMGCostLabel")
		if self.DMGCostLabel:
			self.DMGCostLabel.set_text(f"Стоимость: {self.data['DMGUpgradeCost']}")

	def _on_UpgradeButton_pressed(self):
		global Pause
		Pause = True
		self.get_tree().paused = True
		self.set_pause_state(True)
		self.UpdateMenu.show()

	def _on_UpdateDMGButton_pressed(self):
		cost = self.data.get("DMGUpgradeCost", 10)
		if self.data["Coin"] >= cost:
			self.data["Coin"] -= cost
			self.data["DMG"] += 1
			self.data["DMGUpgradeCost"] = int(cost * 1.5)
			self._save_data()
			self._update_money_label()
			self._update_dmg_label()
			self._update_dmg_cost_label()
			print(f"[Улучшение] Урон увеличен до {self.data['DMG']}, следующее улучшение стоит {self.data['DMGUpgradeCost']}$")
		else:
			print("[Ошибка] Недостаточно денег для улучшения урона!")

	def _on_ExitUpdateMenuButton_pressed(self):
		global Pause
		Pause = False
		self.get_tree().paused = False
		self.set_pause_state(False)
		self.UpdateMenu.hide()

	def _on_MineGuideButton_pressed(self):
		guide = self.get_node("MineGuideButton")
		guide.hide()

	def _on_UpgradeGuideButton_pressed(self):
		guide = self.get_node("UpgradeGuideButton")
		guide.hide()
