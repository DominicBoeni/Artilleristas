from constants import *

class Cannon:
    def __init__(self, x, y, is_left):
        self.x = x
        self.y = y
        self.is_left = is_left
        self.angle = 0 if is_left else 180
        self.power = 25  # Reduced initial power due to increased effectiveness
        self.health = CANNON_HEALTH