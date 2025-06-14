from godot import exposed, Node2D
import json
import os

SAVE_DIR = "save"
CURRENT_SAVE_FILE = f"{SAVE_DIR}/CurrentSaveDir.json"

@exposed
class Tile(Node2D):
	def _ready(self):
		self.current_save_path = self._get_current_save_file()
		self.data = self._load_data()

		self.animated_sprite = self.get_node("AnimatedSprite")
		self.static_body = self.get_node("StaticBody2D")
		self.Mining_Block = self.static_body.get_node("Button")
		self.mining_animation_playing = False
		self.HP = 5

	def _on_Button_pressed(self):
		if self.HP > 0:
			self.animated_sprite.play("Mining")
			self.mining_animation_playing = True
			self.Mining_Block.disabled = True

	def _on_animation_finished(self):
		if self.mining_animation_playing:
			if self.animated_sprite.frame == self.animated_sprite.frames.get_frame_count("Mining") - 1:
				
				# ������ Проверяем, не изменился ли файл сохранения
				self._check_save_file()

				dmg = self.data.get("DMG", 1)
				self.HP -= dmg

				if self.HP <= 0:
					self.data["Coin"] = self.data.get("Coin", 0) + 1
					self._save_data()
					self.queue_free()
				else:
					self.animated_sprite.play("Idle")
			self.mining_animation_playing = False
		self.Mining_Block.disabled = False

	def _get_current_save_file(self):
		try:
			if not os.path.exists(CURRENT_SAVE_FILE):
				return f"{SAVE_DIR}/Save1.json"

			with open(CURRENT_SAVE_FILE, "r") as f:
				data = json.load(f)
				path = data.get("current_save", f"{SAVE_DIR}/Save1.json")
				return path
				
		except Exception as e:
			print(f"[Ошибка] Не удалось прочитать CurrentSaveDir.json: {e}")
			return f"{SAVE_DIR}/Save1.json"

	def _load_data(self):
		"""Загружает данные из текущего файла сохранения"""
		current_save_path = self._get_current_save_file()
	
		if not os.path.exists(current_save_path):
			default_data = {"Coin": 0, "DMG": 1, "DMGUpgradeCost": 10}
			self._save_data(default_data)
			return default_data
	
		with open(current_save_path, "r") as f:
			content = f.read().strip()
			if not content:
				default_data = {"Coin": 0, "DMG": 1, "DMGUpgradeCost": 10}
				self._save_data(default_data)
				return default_data
	
			try:
				data = json.loads(content)
				# Устанавливаем значения по умолчанию для отсутствующих полей
				data.setdefault("Coin", 0)
				data.setdefault("DMG", 1)
				data.setdefault("DMGUpgradeCost", 10)
				return data
			except json.JSONDecodeError:
				print(f"[Ошибка] JSON повреждён в {current_save_path}, создаём дефолтные данные...")
				default_data = {"Coin": 0, "DMG": 1, "DMGUpgradeCost": 10}
				self._save_data(default_data)
				return default_data

	def _check_save_file(self):
		"""Проверяет, не изменился ли файл сохранения с момента последней загрузки"""
		current_save_path = self._get_current_save_file()
	
		if not os.path.exists(current_save_path):
			return
	
		with open(current_save_path, "r") as f:
			content = f.read().strip()
			if not content:
				return
	
			try:
				new_data = json.loads(content)
				new_data.setdefault("Coin", 0)
				new_data.setdefault("DMG", 1)
				new_data.setdefault("DMGUpgradeCost", 10)
	
				# Сравниваем только нужные поля
				if (new_data.get("Coin") != self.data.get("Coin") or
					new_data.get("DMG") != self.data.get("DMG") or
					new_data.get("DMGUpgradeCost") != self.data.get("DMGUpgradeCost")):
	
					# Обновляем только необходимые поля
					self.data["Coin"] = new_data.get("Coin", self.data["Coin"])
					self.data["DMG"] = new_data.get("DMG", self.data["DMG"])
					self.data["DMGUpgradeCost"] = new_data.get("DMGUpgradeCost", self.data["DMGUpgradeCost"])
					print("[INFO] Данные обновлены из файла сохранения.")
			except json.JSONDecodeError:
				print(f"[Ошибка] Не удалось разобрать файл {current_save_path} во время проверки.")

	def _save_data(self, data=None):
		"""Сохраняет данные в текущий файл"""
		current_save_path = self._get_current_save_file()
	
		os.makedirs(SAVE_DIR, exist_ok=True)
	
		# Гарантируем наличие всех ключевых полей перед записью
		save_data = data or self.data
		save_data.setdefault("Coin", 0)
		save_data.setdefault("DMG", 1)
		save_data.setdefault("DMGUpgradeCost", 10)
	
		with open(current_save_path, "w") as f:
			json.dump(save_data, f, indent=4)
