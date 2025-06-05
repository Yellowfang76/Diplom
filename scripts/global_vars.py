from godot import exposed, Node

@exposed
class GlobalVars(Node):
	Coin = 0

	def _init(self):
		# Конструктор (опционально)
		print("GlobalVars initialized")

	def save_game(self):
		try:
			with open("res://save/Save/data.save", "w") as file:
				file.write(str(self.Coin))
			print("Game saved!")
		except Exception as e:
			print("Error saving game:", e)

	def load_game(self):
		try:
			with open("res://save/Save/data.save", "r") as file:
				self.Coin = int(file.read())
			print("Game loaded!")
		except Exception as e:
			print("Error loading game:", e)
