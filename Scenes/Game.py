from godot import exposed, export
from godot import *

global Coin
Coin = 0
save=""
save_path = "res://save/Save/" + str(save) + ".save"


@exposed
class Game(Node2D):
	def _ready(self):
		self.popup = self.get_node("CanvasLayer")
		self.money_label = self.popup.get_node("MoneyLabel")
		Money = 'MONEY: ' + str(Coin)
		self.money_label.set_text(Money)
		
	def _process(self, delta):
		if Input.is_action_just_pressed("ui_shift"):
			global Coin
			Coin += 1
			Money = 'MONEY: ' + str(Coin)
			self.money_label.set_text(Money)
	
