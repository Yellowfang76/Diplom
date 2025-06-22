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

		hp_bonus = self.data.get("HPBonus", 0)
		self.HP = 5 + hp_bonus

	def _on_Button_pressed(self):
		if self.HP > 0:
			self.animated_sprite.play("Mining")
			self.mining_animation_playing = True
			self.Mining_Block.disabled = True

	def _on_animation_finished(self):
		if self.mining_animation_playing:
			if self.animated_sprite.frame == self.animated_sprite.frames.get_frame_count("Mining") - 1:

				self._check_save_file()

				dmg = self.data.get("DMG", 1)
				self.HP -= dmg

				if self.HP <= 0:
					self.data["Coin"] = self.data.get("Coin", 0) + 1

					self.data["BrokenBlocks"] = self.data.get("BrokenBlocks", 0) + 1
					broken_blocks = self.data["BrokenBlocks"]

					if broken_blocks % 100 == 0 and broken_blocks != 0:
						self.data["HPBonus"] = self.data.get("HPBonus", 0) + 1
						print(f"[INFO] Все блоки получают +1 HP! Текущий бонус: {self.data['HPBonus']}")

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
		current_save_path = self._get_current_save_file()
	
		if not os.path.exists(current_save_path):
			default_data = {"Coin": 0, "DMG": 1, "DMGUpgradeCost": 10, "BrokenBlocks": 0, "HPBonus": 0}
			self._save_data(default_data)
			return default_data
	
		with open(current_save_path, "r") as f:
			content = f.read().strip()
			if not content:
				default_data = {"Coin": 0, "DMG": 1, "DMGUpgradeCost": 10, "BrokenBlocks": 0, "HPBonus": 0}
				self._save_data(default_data)
				return default_data
	
			try:
				data = json.loads(content)
				data.setdefault("Coin", 0)
				data.setdefault("DMG", 1)
				data.setdefault("DMGUpgradeCost", 10)
				data.setdefault("BrokenBlocks", 0)
				data.setdefault("HPBonus", 0)
				return data
			except json.JSONDecodeError:
				print(f"[Ошибка] JSON повреждён в {current_save_path}, создаём дефолтные данные...")
				default_data = {"Coin": 0, "DMG": 1, "DMGUpgradeCost": 10, "BrokenBlocks": 0, "HPBonus": 0}
				self._save_data(default_data)
				return default_data

	def _check_save_file(self):
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
					print("[INFO] Данные обновлены из файла сохранения.")
			except json.JSONDecodeError:
				print(f"[Ошибка] Не удалось разобрать файл {current_save_path} во время проверки.")

	def _save_data(self, data=None):
		current_save_path = self._get_current_save_file()
	
		os.makedirs(SAVE_DIR, exist_ok=True)
	
		save_data = data or self.data
		save_data.setdefault("Coin", 0)
		save_data.setdefault("DMG", 1)
		save_data.setdefault("DMGUpgradeCost", 10)
		save_data.setdefault("BrokenBlocks", 0)
		save_data.setdefault("HPBonus", 0)
	
		with open(current_save_path, "w") as f:
			json.dump(save_data, f, indent=4)
