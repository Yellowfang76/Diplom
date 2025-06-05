import os

Coin = 0

save_path = "res://save/data.save"

def save_game():
	global Coin
	try:
		with open(save_path, "w") as file:
			file.write(str(Coin))
		print("Game saved!")
	except Exception as e:
		print("Error saving game:", e)


def load_game():
	global Coin
	try:
		with open(save_path, "r") as file:
			Coin = int(file.read())
		print("Game loaded!")
	except Exception as e:
		print("Error loading game:", e)
