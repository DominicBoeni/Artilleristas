from constants import *

class Square:
    def __init__(self, x, y, type='stone'):
        self.x = x
        self.y = y
        self.type = type
        self.health = 50 if type == 'stone' else (GROUND_HEALTH if type == 'ground' else 0)