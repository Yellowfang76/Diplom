from godot import exposed, export
from godot import *
import json, os

SAVE_DIR = "save"
SAVE_FILE = f"{SAVE_DIR}/CurrentSaveDir.json"

@exposed
class Menu(Node2D):

	def _ready(self):
		self.popup = self.get_node("Panel")

		self.Save1Control = self.popup.get_node("Save1Control")
		self.Save1CoinLabel = self.Save1Control.get_node("Save1CoinLabel")

		self.Save2Control = self.popup.get_node("Save2Control")
		self.Save2CoinLabel = self.Save2Control.get_node("Save2CoinLabel")

		self.Save3Control = self.popup.get_node("Save3Control")
		self.Save3CoinLabel = self.Save3Control.get_node("Save3CoinLabel")

		self.load_save_data()

	def load_save_data(self):
		self._load_and_update_label(f"{SAVE_DIR}/Save1.json", self.Save1CoinLabel)
		self._load_and_update_label(f"{SAVE_DIR}/Save2.json", self.Save2CoinLabel)
		self._load_and_update_label(f"{SAVE_DIR}/Save3.json", self.Save3CoinLabel)

	def _load_and_update_label(self, file_path, label_node):
		try:
			if not os.path.exists(file_path):
				label_node.text = "0"
				return

			with open(file_path, "r") as f:
				content = f.read()
				if not content.strip():
					label_node.text = "0"
					return

				data = json.loads(content)
				coins = data.get("Coin", 0)
				label_node.text = str(coins)

		except (json.JSONDecodeError, IOError) as e:
			print(f"[Ошибка] Не удалось загрузить {file_path}: {e}")
			label_node.text = "0"

	def _on_LoadButton_pressed(self):
		self.popup.show()

	def _on_BackButton_pressed(self):
		self.popup.hide()

	def _on_LoadSave1Button_pressed(self):
		self._set_current_save(f"{SAVE_DIR}/Save1.json")
		self.get_tree().change_scene("res://Scenes/Game.tscn")

	def _on_LoadSave2Button_pressed(self):
		self._set_current_save(f"{SAVE_DIR}/Save2.json")
		self.get_tree().change_scene("res://Scenes/Game.tscn")

	def _on_LoadSave3Button_pressed(self):
		self._set_current_save(f"{SAVE_DIR}/Save3.json")
		self.get_tree().change_scene("res://Scenes/Game.tscn")

	def _set_current_save(self, save_path):
		os.makedirs(SAVE_DIR, exist_ok=True)
		with open(SAVE_FILE, "w") as f:
			json.dump({"current_save": save_path}, f)

	def _on_ExitButton_pressed(self):
		self.get_tree().quit()
