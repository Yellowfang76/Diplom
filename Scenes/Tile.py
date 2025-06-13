from godot import exposed, Node2D
import json, os

SAVE_DIR = "save"
CURRENT_SAVE_FILE = f"{SAVE_DIR}/CurrentSaveDir.json"

@exposed
class Tile(Node2D):
	_data = None
	_current_save_path = None

	def _ready(self):
		if Tile._data is None or Tile._current_save_path != self._get_current_save_file():
			Tile._current_save_path = self._get_current_save_file()
			Tile._data = self._load_data()

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
				dmg = Tile._data.get("DMG", 1)
				self.HP -= dmg

				if self.HP <= 0:
					Tile._data["Coin"] = Tile._data.get("Coin", 0) + 1
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
			default_data = {"Coin": 0, "DMG": 1}
			self._save_data(default_data)
			return default_data

		with open(current_save_path, "r") as f:
			content = f.read().strip()
			if not content:
				default_data = {"Coin": 0, "DMG": 1}
				self._save_data(default_data)
				return default_data

			try:
				return json.loads(content)
			except json.JSONDecodeError:
				print(f"[Ошибка] JSON повреждён в {current_save_path}, создаём дефолтные данные...")
				default_data = {"Coin": 0, "DMG": 1}
				self._save_data(default_data)
				return default_data

	def _save_data(self, data=None):
		"""Сохраняет данные в текущий файл"""
		current_save_path = self._get_current_save_file()

		os.makedirs(SAVE_DIR, exist_ok=True)
		with open(current_save_path, "w") as f:
			json.dump(data or Tile._data, f, indent=4)
