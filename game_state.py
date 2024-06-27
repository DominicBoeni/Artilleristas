import random
from constants import WIND_MIN, WIND_MAX

class GameState:
    def __init__(self, player1, player2, ground):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.ground = ground
        self.game_over = False
        self.current_wind = 0

    def switch_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def update_wind(self):
        self.current_wind = random.randint(WIND_MIN, WIND_MAX)


    def end_turn(self):
        self.current_player.add_coin()
        self.update_wind()
        self.current_player.repair_mode = False
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1
        if self.current_player.cannons:
            self.current_player.selected_cannon = 0
        else:
            self.game_over = True
